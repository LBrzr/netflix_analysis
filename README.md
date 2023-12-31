# Netflix Analytics with Python, Pandas, Matplotlib, Hadoop Spark, Docker, and Docker Compose

## Project Overview

This school project focuses on analyzing and visualizing Netflix data using Python, Pandas, and Matplotlib, integrated into a Hadoop Spark pipeline. The entire project is containerized using Docker and orchestrated with Docker Compose, allowing for easy deployment and scalability.

## Features

1. **Dockerized Environment:** The project is encapsulated within Docker containers, ensuring consistent and reproducible environments across different systems.

2. **Hadoop Spark Processing:** Leverage the power of Hadoop Spark for efficient and distributed data processing within a Docker container.

3. **Pandas for Data Manipulation:** Utilize the Pandas library for data manipulation and preprocessing within a Docker container.

4. **Matplotlib for Visualization:** Create informative and visually appealing plots using Matplotlib within a Docker container.

5. **Docker Compose Orchestration:** Use Docker Compose for seamless orchestration of multiple containers, simplifying deployment and management.

6. **Sample Netflix Analytics:**
   - **Popular Genres**.
   - **Movies and TV Shows mean durations**.

## Technologies Used

- **Python:** The primary programming language for data manipulation, analysis, and visualization.

- **Pandas:** A powerful data manipulation library for cleaning and preprocessing the Netflix dataset.

- **Matplotlib:** A comprehensive plotting library for creating a variety of visualizations.

- **Hadoop Spark:** A distributed computing framework for efficient big data processing.

- **Docker:** Containerization platform for packaging the entire project.

- **Docker Compose:** Tool for defining and running multi-container Docker applications.

## How to Run the Project

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/LBrzr/netflix_analysis.git
   ```

2. **Navigate to the Project Folder:**
   ```bash
   cd netflix_analysis
   ```

3. **Build and Run with Docker Compose:**
   ```bash
   cd docker
   docker-compose up --build
   ```
   
4. **Run analysis script**
   ```bash
   python calcul.py
   ``` 
  
5. **Explore the Results:**
   - Open the generated plots in the `chart_images/` folder to explore the Netflix analytics insights.

## Contributors

- **Danny WANG:** Developer and analyst.
- **Melanie Le CLEUZIAT:** Developer and analyst.
- **Wassim HOUIAT:** Developer and analyst.
- **Saif MEROUAR:** Developer and analyst.
- **Leandre AKAKPO:** Developer and analyst.

## Feedback and Contributions

We welcome feedback and contributions to enhance the Netflix Analytics project. Feel free to open issues, submit pull requests, or provide insights into improving the analysis.

Thank you for exploring the world of Netflix data with us! 🍿📊
