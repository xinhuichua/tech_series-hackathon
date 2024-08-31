# SCRUMptious avengers

## Proposed Solution
We are proposing a comprehensive solution to enhance the quality of life for the ageing population by improving access to healthcare, fostering social engagement, and providing daily living and emergency assistance. 

## Features Implemented in Our Application
### Feature 1
- Moderated and Regulated Chatrooms to encourage befriending and promote engagement with other seniors

### Feature 2
- Emergency SOS Button Integration for Fall Prevention
=====
To be able to receive messages:
1. Send </start> to the bot: https://t.me/ElderCareAlertBot
2. Send a Message to the following bot. i.e. Hello
3. Retrieve Chat id via: https://tinyurl.com/checkChatID
4. Replace Chat id with your Chat id. There are two chat ids to replace, one in SOS.vue (line 35) and another in homepage.vue (line 133)
  
### Feature 3
- Personalized Daily Routine and Medication Management for Seniors

## Key Technologies Used to Develop the Website
Vue, Python, HTML

## Steps to run the application
### 1. Install the required packages
```
npm install
```
```
pip install flask_cors
```

### 2. Open 3 terminals

* First Terminal:
  * Run the Python script:
    ```
    cd agecare-app
    ```
    ```
    python MedicineData.py
    ```

* Second Terminal
  * Run the Python script:
    ```
    cd agecare-app
    ```
    ```
    python ChatRoom.py
    ```
* Third Terminal:
  * Navigate to the application directory
    ```
    cd agecare-app
    ```
  * Run the app
    ```
    npm run dev
    ```

## Helpful references
- [Vue.js] (https://vuejs.org/)
- [Vue Boostrap] (https://bootstrap-vue.org/)
- [Telegram API] (https://core.telegram.org/)

## Developers
### Chua Xinyan
### Lee Jia Wen
### Amanda Ong Qian Ying
### Soh Wen Jie
### Chua Xinhui
