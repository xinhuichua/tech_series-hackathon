# SCRUMptious avengers

## Proposed Solution
We are proposing a comprehensive solution to enhance the quality of life for the ageing population by improving access to healthcare, fostering social engagement, and providing daily living and emergency assistance. 

## Features Implemented in Our Application
### Feature 1
- Moderated and Regulated Chatrooms to encourage befriending and promote engagement with other seniors

### Feature 2
- Emergency SOS Button Integration for Fall Prevention
To be able to receive messages:
1. Send a Message to the following bot: https://t.me/ElderCareAlertBot
2. Retrieve Chat id via: https://api.telegram.org/bot7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI/getUpdates?offset=6845319
3. Replace Chat id in line 35 with your Chat id
  
### Feature 3
- Medication Notification for Seniors

## Technologies Used to Develop the Website
Vue, Python

## Steps to run the application
1. Install the requried packages
```
npm install
```

2. Open 3 terminals

* First Terminal:
  * Run the Python script:
    ```
    python MedicineData.py
    ```

* Second Terminal
  * Run the Python script:
  ```
  run MedicineData.py
  ```
* Third Terminal:
  * Navigate to the application directory
```
cd agecare-app
```

3. Run the app
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
