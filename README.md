# Word Puzzle API

A FastAPI-based API that serves random lines from word files.

## Endpoints

- `GET /get6` - Returns a random line from 6-word.txt
- `GET /get8` - Returns a random line from 8-word.txt
- `GET /get10` - Returns a random line from 10-word.txt
- `GET /puzzle` - Returns a random line from each word file
- `GET /` - Shows API documentation and status

## VPS Deployment Instructions

1. Clone the repository to your VPS:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install Python and pip if not already installed:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Set up systemd service for running the API:

Create a service file:
```bash
sudo nano /etc/systemd/system/wordpuzzle.service
```

Add the following content (adjust paths as needed):
```ini
[Unit]
Description=Word Puzzle API
After=network.target

[Service]
User=<your-user>
WorkingDirectory=/path/to/api
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Start and enable the service:
```bash
sudo systemctl start wordpuzzle
sudo systemctl enable wordpuzzle
```

6. (Optional) Set up Nginx as a reverse proxy:

Install Nginx:
```bash
sudo apt install nginx
```

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/wordpuzzle
```

Add the configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/wordpuzzle /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## API Response Format

For /get6, /get8, and /get10 endpoints:
```json
{
    "line": "example line of text"
}
```

For /puzzle endpoint:
```json
{
    "6_word_line": "example line from 6-word.txt",
    "8_word_line": "example line from 8-word.txt",
    "10_word_line": "example line from 10-word.txt"
}
```

The root endpoint (/) returns API documentation and status:
```json
{
    "message": "Word Puzzle API",
    "endpoints": {
        "/get6": "Get a random 6-word line",
        "/get8": "Get a random 8-word line",
        "/get10": "Get a random 10-word line",
        "/puzzle": "Get a random line from each word list"
    },
    "status": {
        "6_word_lines": 3,
        "8_word_lines": 3,
        "10_word_lines": 3
    }
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Successful request
- 500: Server error (e.g., file not found, no entries available)

## File Structure
```
.
├── main.py           # Main API implementation
├── requirements.txt  # Python dependencies
├── 6-word.txt       # Source file for 6-word lines
├── 8-word.txt       # Source file for 8-word lines
├── 10-word.txt      # Source file for 10-word lines
└── README.md        # This documentation