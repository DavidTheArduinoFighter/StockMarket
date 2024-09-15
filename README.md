# 📈 Stock Market Data Library

**Author**: David Ogorevc  
**License**: Free to use, no warranties provided. Use at your own risk.  
**GitHub**: [Your GitHub Account]

---

## 📝 Project Description


This project is a simple Python library designed to provide stock market data. With this data, you can program your own trading strategies in Python and test them on real historical data. In future versions, I plan to add methods for graphical displays and calculating gains/losses compared to the market benchmark (e.g., S&P 500).

Unlike most stock data sources, which either charge fees or limit free API calls, I built my own database to store stock data for easy and unrestricted access. I used the **TwelveData API**, which allows up to 800 free API calls per day (as of 09/2024), with additional rate limits per minute. The data includes:
- Open/Close prices
- High/Low prices for each time interval
- Trading volume

The data is collected in **15-minute intervals** from the **Nasdaq stock exchange**.

This project was created for friends and acquaintances who have basic Python knowledge but are not professional developers. Users can select stocks, ETFs, and a benchmark (e.g., S&P 500) through the UI, retrieve pre-stored stock data, and experiment with it.

At the time of writing, I am a junior electrical engineer starting to explore this kind of programming. While I know the project could be improved, it's functional and provides the core capabilities I aimed for. Future updates will enhance usability and functionality.

The project has been successfully tested on **Windows 10** and **11**, but there are issues with **Linux (Zorin OS)** due to an unsupported MariaDB library.

---

## 🛠️ Installation Steps

### Required Software:
- [Python](https://www.python.org/downloads/)
- [PyCharm Community Edition (Recommended)](https://www.jetbrains.com/pycharm/download/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [X server for Windows (VcXsrv)](https://sourceforge.net/projects/vcxsrv/)

### Setup Instructions:

#### 1. Create a PyCharm Project
- Create a new project in PyCharm and set up a virtual environment.
- Copy the files from this repository into your new project.

#### 2. Set Up TwelveData API
- Go to the [TwelveData](https://twelvedata.com/) website and create an account.
- Generate an API token.
- Place the token in the `docker/api/json/credentials/twelveCredentials.json` file, replacing `<your_token>`. Also, set the database username, password, and database name (or leave the default settings, though changes are recommended).

#### 3. Build the Library
- Open the terminal in PyCharm and run the following commands (paste and hit enter):
    ```
    python setup.py sdist bdist_wheel
    pip install .
    ```

#### 4. Set Up X Server (for running the UI in Docker)
- Install and run **X server (VcXsrv)**:
  - Start XLaunch: 
    - Display Settings -> Next
    - Client Startup -> Next
    - Extra Settings -> Check all boxes -> Next
   
      ![image](https://github.com/user-attachments/assets/175071f6-34ce-49f5-9977-b2a9d9f2f667)

  - Save the configuration and click **Finish**.
  - Open the saved configuration file and double-click to run it.
  - Ensure the X server icon appears in the taskbar. Test it by running an application (right-click, and open one of the apps).

    ![image](https://github.com/user-attachments/assets/f836fb5c-aaab-4d64-a406-93754b4de665)


#### 5. Run Docker
- Open Docker Desktop (ensure **WSL** is installed as well) ([WSL Installation](https://learn.microsoft.com/en-us/windows/wsl/install)).
- In the terminal, run:
    ```
    docker compose up -d
    ```
- Ensure you're connected to the internet for Docker to download and build containers.

---

## 🚀 UI Launch

Once the X server is running correctly, the UI window will open. You can start testing by entering a stock or ETF ticker and a benchmark (e.g., S&P 500).


- Add as many stocks or ETFs as you like. The benchmark will be replaced if a new one is entered.
- After selecting stocks, navigate to the second tab and click "Update Database." This process may take several minutes, depending on the number of stocks selected (limited by free API calls from TwelveData).
- The UI may appear unresponsive during the update (normal due to the lack of multi-threading support).

![image](https://github.com/user-attachments/assets/f44aca68-f899-4724-b029-5d1436d12e36)

![image](https://github.com/user-attachments/assets/772e799b-9612-4cfc-a2e0-177d894835d3)

Once the update is complete, the you will be notified, and you can close the program. To relaunch the program, go to Docker Desktop and click "play" on the container. 
The other two connectors need to be active (green status) at all times for the Python library to operate properly.

![image](https://github.com/user-attachments/assets/20b111c5-ca0b-49aa-a89a-444e90276d47)

---

## ▶️ How to Run `main.py`

Once everything is set up, you can run the `main.py` script to start using the library. It provides an example of how to retrieve stock data for a specified ticker. 
This data can be the foundation for building and testing your own trading strategy.

Now you're ready to explore and develop your own trading strategies with real stock market data. Good luck! 🚀📊

---

## ⚖️ License

This project is free and available for everyone. However, no warranties are provided. Use this library at your own risk, and I am not responsible for any issues or financial losses that may arise from its use.
