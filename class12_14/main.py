#main.py

from http.client import HTTPException
import pathlib

from fastapi import FastAPI, Query, File, UploadFile, HTTPException
import logging
import io
import pandas as pd
from src import MovieInput, MovieResponse, CSVInfo, DataStorage


app = FastAPI(title="Movie API")
storage = DataStorage() # Create a single instance of DataStorage to be used across requests.


@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}

from src import MovieInput

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump() #Converts the model to a Python dictionary.

from src import MovieResponse

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record #expects one movie, change to [record] for multiple


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # TODO 1: return up to limit movies as a list.
    movie_list = list(movies.values())[:limit]
    # Log the number returned at INFO.
    logger.info(f"Returning {len(movie_list)} movies.")
    return movie_list


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # TODO 2: 
    # Convert movie to a dictionary, add the new ID, and store it.
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    # Log the new ID at INFO and return the stored record.
    logger.info(f"Adding movie with ID: {movie_id}")
    return record

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):

        if pathlib.Path(file.filename).suffix == ".csv":
            contents = await file.read()

            try:
                df = pd.read_csv(io.BytesIO(contents))
            except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError, AttributeError) as e:
                logger.warning(f"Error parsing CSV file: {file.filename}, error: {str(e)}")
                raise HTTPException(status_code=400, detail="Error parsing CSV file")
            
            dataset_id = storage.save_data(df, file.filename)
            logger.info(f"CSV file stored with dataset_id: {dataset_id} and filename: {file.filename}")
            
            return CSVInfo(
                filename=file.filename,
                rows=df.shape[0],
                columns=df.shape[1],
                column_names=list(df.columns),
                dataset_id=dataset_id
            )
        else:
            logger.warning(f"File is Not a CSV: {file.filename}")
            raise HTTPException(status_code=400, detail="File is Not a CSV")

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # TODO 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    stored_df = storage.get_data(dataset_id)
    
    if stored_df is None:
        logger.warning(f"Dataset not found: {dataset_id}")
        raise HTTPException(status_code=404, detail="Dataset not found")
   
    return {
            "dataset_id": dataset_id,
            "rows": stored_df.shape[0],
            "columns": stored_df.shape[1]
            }
    

    
