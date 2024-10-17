import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
import psycopg2
from psycopg2 import sql
from database import get_db_connection  # Import your custom database connection function
from dotenv import load_dotenv  # Import to load environment variables

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize the Flask app
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Define a resource for fetching weather data
class Weather(Resource):
    def get(self):
        """
        Get weather data for a specific station and date.
        ---
        parameters:
          - name: station_id
            in: query
            type: string
            required: false
            description: The ID of the weather station.
          - name: date
            in: query
            type: string
            required: false
            description: The date for which to fetch the weather data (YYYY-MM-DD).
          - name: page
            in: query
            type: integer
            required: false
            description: Page number for pagination (default is 1).
          - name: per_page
            in: query
            type: integer
            required: false
            description: Number of records per page (default is 10).
        responses:
          200:
            description: A list of weather data with pagination info.
            schema:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total_records:
                  type: integer
                total_pages:
                  type: integer
                has_next:
                  type: boolean
                has_previous:
                  type: boolean
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      station_id:
                        type: string
                      date:
                        type: string
                      max_temp:
                        type: number
                      min_temp:
                        type: number
                      precipitation:
                        type: number
        """
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        query = "SELECT station_id, date, max_temp, min_temp, precipitation FROM weather_data WHERE TRUE"
        params = []

        if station_id:
            query += " AND station_id = %s"
            params.append(station_id)
        
        if date:
            query += " AND date = %s"
            params.append(date)

        # Count query to get total number of records
        count_query = sql.SQL(query).as_string(conn).replace("SELECT station_id, date, max_temp, min_temp, precipitation", "SELECT COUNT(*)")
        cur.execute(count_query, params)
        total_records = cur.fetchone()[0]

        offset = (page - 1) * per_page
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, offset])

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        total_pages = (total_records + per_page - 1) // per_page
        has_next = page < total_pages
        has_previous = page > 1

        data = [
            {
                'station_id': row[0],
                'date': row[1],
                'max_temp': row[2],
                'min_temp': row[3],
                'precipitation': row[4]
            }
            for row in rows
        ]

        response = {
            'page': page,
            'per_page': per_page,
            'total_records': total_records,
            'total_pages': total_pages,
            'has_next': has_next,
            'has_previous': has_previous,
            'data': data
        }

        return jsonify(response)

# Define a resource for fetching yearly weather statistics
class WeatherStats(Resource):
    def get(self):
        """
        Get yearly weather statistics for all stations.
        ---
        responses:
          200:
            description: A list of yearly weather statistics.
            schema:
              type: array
              items:
                type: object
                properties:
                  station_id:
                    type: string
                  year:
                    type: integer
                  avg_max_temp:
                    type: number
                  avg_min_temp:
                    type: number
                  total_precipitation:
                    type: number
        """
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT station_id, year, avg_max_temp, avg_min_temp, total_precipitation FROM yearly_weather_stats")
        rows = cur.fetchall()

        stats_data = [
            {
                'station_id': row[0],
                'year': row[1],
                'avg_max_temp': row[2],
                'avg_min_temp': row[3],
                'total_precipitation': row[4]
            }
            for row in rows
        ]

        cur.close()
        conn.close()

        return jsonify(stats_data)

# Define API routes
api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
