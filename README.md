# Code Challenge Template

```markdown
# Weather Data Ingestion and API

This project ingests weather data from text files, performs basic analysis, and exposes the data through a REST API built with Flask.

## Features

* **Data Ingestion:** Reads weather data from text files and stores it in a PostgreSQL database.
* **Data Analysis:** Calculates yearly weather statistics (average maximum temperature, average minimum temperature, total precipitation).
* **REST API:** Provides endpoints to retrieve weather data and yearly statistics.
* **Filtering and Pagination:** API endpoints support filtering by station ID and date, as well as pagination for large datasets.
* **Swagger/OpenAPI Documentation:** API documentation is automatically generated using Swagger/OpenAPI, accessible at `/apidocs/`.

## Getting Started

### Prerequisites

* Python 3.7+
* PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repository-url>
   cd weather-data-api 
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL:**
   * Create a database.
   * Create a user with appropriate permissions for the database.

5. **Configure environment variables:**
   * Create a `.env` file in the project's root directory.
   * Add the following environment variables, replacing placeholders with your database credentials:

     ```
     DB_NAME=<your_database_name>
     DB_USER=<your_database_user>
     DB_PASSWORD=<your_database_password>
     DB_HOST=<your_database_host> 
     DB_PORT=<your_database_port> 
     DATABASE_URL=postgresql://weather_user:root@localhost:5432/weather_data
     ```

6. **Create database tables:**

   ```bash
   python create_tables.py
   ```

7. **Ingest data:**

   ```bash
   python injest_data.py
   ```

### Running the API

```bash
python api.py
```

The API will be accessible at `http://127.0.0.1:5000/`.

### API Documentation

Swagger/OpenAPI documentation is available at `http://127.0.0.1:5000/apidocs/`.

## API Endpoints

* **`/api/weather`:**
    * **GET:** Retrieve weather data.
      * Query parameters:
        * `station_id`: Filter by station ID.
        * `date`: Filter by date (YYYY-MM-DD).
        * `page`: Page number for pagination (default: 1).
        * `per_page`: Number of items per page (default: 10).
* **`/api/weather/stats`:**
    * **GET:** Retrieve yearly weather statistics.

## Example API Usage

**Get weather data for station USC00110034 on 2010-01-01:**

```
http://127.0.0.1:5000/api/weather?station_id=USC00110034&date=2010-01-01
```

**Get yearly weather statistics:**

```
http://127.0.0.1:5000/api/weather/stats
```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

**Changes for GitHub Friendliness:**

* **Clearer Structure:** Uses headings and lists to improve readability.
* **Concise Language:** Provides essential information without being overly verbose.
* **Code Blocks:** Uses code blocks for commands and examples.
* **Links:** Includes links to relevant files (e.g., LICENSE).
* **Visual Appeal:** Uses formatting (bold, italics) to highlight important information.

This updated README.md is more concise and easier to navigate, making it ideal for sharing on GitHub.
