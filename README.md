<body>
   <h1>ChitChat SpamBot</h1>
    <p>This bot allows users to send spam messages and promotions on <strong>ChitChat.gg</strong>.</p>
  
 <h2>Disclaimer</h2>
        <p>This spambot is intended for educational purposes only. The creator is not responsible for any misuse or illegal activities conducted with this bot. By using this script, you agree to use it in a lawful manner and to respect the terms of service of ChitChat.gg. If you use this bot for malicious purposes, you do so at your own risk.</p>
   <h2 id="features">Features</h2>
    <ul>
        <li>Send messages using multiple auth tokens.</li>
        <li>Save and manage auth tokens in a text file.</li>
        <li>Update Chrome user data paths easily.</li>
        <li>Customizable message sending iterations.</li>
    </ul>

   <h2 id="installation">Installation</h2>
    <pre><code>git clone https://github.com/garurprani/ChitChat-spambot.git
cd ChitChat-spambot
pip install -r requirements.txt
    </code></pre>
    <p>Make sure to have Chrome and <strong>chromedriver</strong> installed and accessible in your system's PATH.</p>

  <h2 id="usage">Usage</h2>
    <p>1. Run the script using Python:</p>
    <pre><code>python main.py
    </code></pre>
    <p>2. Follow the on-screen instructions to:</p>
    <ul>
        <li>Add Auth Tokens</li>
        <li>Show Auth Tokens</li>
        <li>Update the profile path</li>
        <li>Run the spam script</li>
    </ul>

  <p>This tutorial will guide you through the process of setting up and running a Python script using Selenium to automate browser actions.</p>

   <div class="step">
            <h2 class="step-title">Step 1: Install Required Packages</h2>
            <p>Ensure you have the required Python packages installed. You can install them using pip:</p>
            <pre><code>pip install requests psutil selenium</code></pre>
        </div>

  <div class="step">
            <h2 class="step-title">Step 2: Replace <code>user_data_dir</code> and <code>auth_token</code></h2>
            <h3>Replace <code>user_data_dir</code></h3>
            <ol>
                <li>Open your Chrome browser and type <code>chrome://version/</code> in the address bar.</li>
                <li>Find the <strong>Profile Path</strong>. It should look something like <code>C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data</code>.</li>
                <li>Copy this path and replace the value of <code>user_data_dir</code> in the code:</li>
            </ol>
            <pre><code>user_data_dir = "C:/Users/&lt;YourUsername&gt;/AppData/Local/Google/Chrome/User Data"</code></pre>
            
   <h3>Replace <code>profile_directory</code></h3>
            <ol>
                <li>Identify the profile you want to use (e.g., <code>Profile 1</code>, <code>Profile 2</code>, etc.).</li>
                <li>Replace the value of <code>profile_directory</code> in the code:</li>
            </ol>
            <pre><code>profile_directory = "Profile 5"  <!-- Replace with your profile number --></code></pre>
     <h3>Replace <code>auth_token</code></h3>
            <ol>
                <li>Obtain your authentication token from the relevant source.</li>
                <li>Replace the <code>auth_token</code> value in the <code>main</code> function:</li>
            </ol>
            <pre><code>auth_token = "your_actual_token_here"</code></pre>
         

   <div class="step">
            <h2 class="step-title">Step 3: Download and Setup ChromeDriver</h2>
            <h3>Find Chrome Version</h3>
            <ol>
                <li>Open Chrome and type <code>chrome://settings/help</code> in the address bar to find your Chrome version.</li>
            </ol>
          
  <h3>Download ChromeDriver</h3>
            <ol>
                <li>Go to the <a href="https://sites.google.com/chromium.org/driver/downloads">ChromeDriver download page</a> and download the version that matches your Chrome browser version.</li>
            </ol>
    <h3>Extract and Place ChromeDriver</h3>
            <ol>
                <li>Extract the downloaded file.</li>
               <li>Place the <code>chromedriver.exe</code> file in the same directory as your script, or provide the correct path in the code:</li>
            </ol>
            <pre><code>webdriver_path = os.path.join(script_dir, 'chromedriver.exe')  <!-- Adjust the path if necessary --></code></pre>
        </div>
   <div class="step">
            <h2 class="step-title">Step 4: Run the Script</h2>
            <p>Ensure the script is in the same directory as <code>chromedriver.exe</code> or the path to <code>chromedriver.exe</code> is correctly set. Then run the script using Python:</p>
            <pre><code>python your_script_name.py</code></pre>
        </div>
  <div class="step">
            <h2 class="step-title">Full Code After Adjustments</h2>
        </div>
    </div>
        <h2 id="contributing">Contributing</h2>
    <p>Contributions are welcome! Please fork the repository and submit a pull request for any improvements or features.</p>
    <p>For major changes, please open an issue first to discuss what you would like to change.</p>


</body>

