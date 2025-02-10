from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Word Puzzle API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load word lists
def load_words(filename: str) -> list[str]:
    try:
        with open(filename, 'r') as f:
            # Read all lines and filter out empty ones
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if not lines:
                raise ValueError(f"No valid lines found in {filename}")
            return lines
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Word file {filename} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading {filename}: {str(e)}")

# Initialize word lists
try:
    words_6 = load_words('6-word.txt')
    words_8 = load_words('8-word.txt')
    words_10 = load_words('10-word.txt')
except Exception as e:
    print(f"Error loading word files: {str(e)}")
    words_6 = []
    words_8 = []
    words_10 = []

@app.get("/get6")
async def get_6_word():
    """Get a random 6-word line"""
    if not words_6:
        raise HTTPException(status_code=500, detail="No 6-word entries available")
    return {"line": random.choice(words_6)}

@app.get("/get8")
async def get_8_word():
    """Get a random 8-word line"""
    if not words_8:
        raise HTTPException(status_code=500, detail="No 8-word entries available")
    return {"line": random.choice(words_8)}

@app.get("/get10")
async def get_10_word():
    """Get a random 10-word line"""
    if not words_10:
        raise HTTPException(status_code=500, detail="No 10-word entries available")
    return {"line": random.choice(words_10)}

@app.get("/puzzle")
async def get_puzzle():
    """Get a random line from each word list"""
    if not all([words_6, words_8, words_10]):
        raise HTTPException(status_code=500, detail="Some word lists are not available")
    return {
        "6_word_line": random.choice(words_6),
        "8_word_line": random.choice(words_8),
        "10_word_line": random.choice(words_10)
    }

@app.get("/")
async def root():
    """API root endpoint with usage information"""
    return {
        "message": "Word Puzzle API",
        "endpoints": {
            "/get6": "Get a random 6-word line",
            "/get8": "Get a random 8-word line",
            "/get10": "Get a random 10-word line",
            "/puzzle": "Get a random line from each word list"
        },
        "status": {
            "6_word_lines": len(words_6),
            "8_word_lines": len(words_8),
            "10_word_lines": len(words_10)
        }
    }