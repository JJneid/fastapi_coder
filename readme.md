# AutoGen FastAPI Wrapper

This FastAPI application wraps AutoGen code generation functionality, providing HTTP endpoints to process tasks and retrieve generated code files.


## Usage

1. Start the FastAPI server:
```bash
python main.py
```
The server will start at `http://localhost:8000`

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Process a Task

```http
POST /process
```

Request body:
```json
{
    "task": "Your task description here"
}
```

Example using curl:
```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"task": "Analyze American Airlines (AAL) stock, include last 2 years of stock data and Calculate basic technical indicators (moving averages, volatility)"}'
```

Response:
```json
{
    "result": "Task execution result here",
    "generated_file": "example_123.py"
}
```

### Retrieve Generated Code

```http
GET /code/{filename}
```

Example using curl:
```bash
curl "http://localhost:8000/code/example_123.py"
```

Response:
```json
{
    "filename": "example_123.py",
    "content": "# Generated Python code content here"
}
```

## Project Structure

```
.
├── main.py           # FastAPI application
├── .env             # Environment variables
├── coding/          # Directory for generated code files
└── README.md        # This file
```

## Error Handling

The API includes proper error handling for common scenarios:

- 404: File not found
- 500: Internal server error
- Invalid request format
- Task processing failures

## Testing

1. Basic endpoint test:
```bash
# Test process endpoint
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"task": "Create a simple hello world program"}'

# Test code retrieval (replace filename)
curl "http://localhost:8000/code/hello_world_123.py"
```

2. Complex task test:
```bash
# Test stock analysis
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"task": "Analyze American Airlines (AAL) stock, include last 2 years of stock data and Calculate basic technical indicators (moving averages, volatility)"}'
```

#

