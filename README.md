# Netflix Content Analytics Dashboard

This repository contains a Dash application for visualizing Netflix content analytics for the year 2023.

## Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- pip

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Vimukthixsandeepa/netflix-content-analytics.git
    cd netflix-content-analytics
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the App

1. Run the Dash app:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:8051/` to view the dashboard.

## Files

- `app.py`: The main script to run the Dash app.
- `data/netflix_content_2023.csv`: The dataset used for the analysis.
- `notebook.ipynb`: Jupyter Notebook containing the data analysis and visualizations.

## Data Cleaning

The dataset is cleaned by replacing commas in the 'Hours Viewed' column and converting it to a float type.

## Visualizations

The dashboard includes the following visualizations:

1. **Total Viewership Hours by Content Type (2023)**
2. **Total Viewership Hours by Language (2023)**
3. **Total Viewership Hours by Release Month (2023)**
4. **Top 5 Titles Based on Viewership Hours**
5. **Viewership Trends by Content Type and Release Month (2023)**
6. **Total Viewership Hours by Release Season (2023)**
7. **Monthly Release Patterns and Viewership Hours (2023)**
8. **Weekly Release Patterns and Viewership Hours (2023)**
9. **Viewership Hours for Releases Near Significant Holidays**

## Deployment

### Local Deployment

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Vimukthixsandeepa/netflix-content-analytics.git
    cd netflix-content-analytics
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Dash app locally:**
    ```sh
    python app.py
    ```

4. **Open your web browser and go to `http://127.0.0.1:8051/` to view the dashboard.**

### Deployment on Heroku

1. **Install the Heroku CLI:**
    Follow the instructions [here](https://devcenter.heroku.com/articles/heroku-cli) to install the Heroku CLI.

2. **Log in to Heroku:**
    ```sh
    heroku login
    ```

3. **Create a new Heroku app:**
    ```sh
    heroku create netflix-content-analytics
    ```

4. **Add a `Procfile`:**
    Create a file named `Procfile` in the root directory of your project with the following content:
    ```
    web: python app.py
    ```

5. **Add a `requirements.txt` file:**
    Ensure you have a `requirements.txt` file in the root directory of your project with all the dependencies listed.

6. **Add a `runtime.txt` file:**
    Create a file named `runtime.txt` in the root directory of your project with the following content:
    ```
    python-3.8.12
    ```

7. **Commit your changes:**
    ```sh
    git add .
    git commit -m "Prepare for Heroku deployment"
    ```

8. **Deploy to Heroku:**
    ```sh
    git push heroku main
    ```

9. **Open your deployed app:**
    ```sh
    heroku open
    ```

Your dashboard should now be live on Heroku!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
