const textBoxArea = document.getElementById("textbox");
const sendButton = document.getElementById("send_button");
const greetingMessage = document.getElementById("greetingMessage");
const menuButton = document.getElementById("menu-button");
const taskSelectionMenu = document.getElementById("task-selection");
const modelCard = document.querySelector(".model_categorization");
const imageClass = document.getElementById("image-class");
const textClassification = document.getElementById("text-class");
const summarizerClass = document.getElementById("summarizer-class");
const responseBody = document.getElementById("responseBody"); 
const modelCards = document.querySelectorAll(".model_card");
const fileUploadButton = document.getElementById("file-uploader");
const fileDisplayIcon = document.getElementById("file-upload-icon");
let defaultEventHandler = null;
let currentButtonListener = null;
let currentKeyupListener = null;

    //Make send button initially disabled
    function disableSendButton(){
      sendButton.disabled = true;
    }
    
    const checkLoadingTime = (element, responseText) => {
        if (!((element === "") || (element === undefined))) {
            // If not empty, return string, and add it to the screen as the response
            responseText.textContent = element;
            addToTextCanva(responseBody, responseText);
            scrollScreen(responseText);
            removeLoadingIcon();
        } else if ((element == "" ||summary == undefined )) {
          setTimeout(() => {
           removeLoadingIcon();
          errorMessage("Timeout Exception");
          }, 30000);   
      }
    }
    //Creating an event listener for imageclass 
    const imageClassEventListener = function() {
      const responseBody = document.getElementById("responseBody"); 
      const modelCategory = document.createElement("section");
      const textOne = ["Leverage the power AI to perform early skin cancer predictions","Leverage the power AI to perform early lung disease classification"];
      const titles = ["Skin Cancer Classifier", "Pneumonia Classifier"];

      //Clear the screen firs    
       //Proceed to add the click button logic
       const imageClassListener = () => {
        modelCategory.classList.add("model_categorization");
          for (let i = 0; i <= 1; i++) { //Need to fix the Pneumonia model in  future update
              const modelArticle = document.createElement("article");
              modelArticle.classList.add("model_card");
              modelArticle.setAttribute("id", `AT${i + 1}`);
              const modelTitle = document.createElement("h3");
              const modelPar = document.createElement("p");
              modelTitle.textContent = titles[i];
              modelPar.textContent = textOne[i];
              modelArticle.appendChild(modelTitle);
              modelArticle.appendChild(modelPar);
              modelCategory.appendChild(modelArticle);
          } 
           //If modelCategory is already a child of responseBody, remove it
          responseBody.appendChild(modelCategory);
          scrollScreen(modelCategory);
          //Then add it back in future iterations to avoid clutter
          modelSelectionEventHandler(modelCategory, responseBody);
        }
      imageClassListener();
  }  

   const removeCurrentListeners = () => {
     if (currentButtonListener) {
       sendButton.removeEventListener("click", currentButtonListener);
       currentButtonListener = null;
     }
     if (currentKeyupListener) {
       textBoxArea.removeEventListener("keyup", currentKeyupListener);
       currentKeyupListener = null;
     }
   };

   const textClassifierEventListener = function () {
      removeCurrentListeners();
      //Check that the file uploader is none
      if (fileDisplayIcon.style.display === "block") {
        fileDisplayIcon.style.display = "none";
      }
      //Inform user of model switch
      const p = document.createElement("p");
      p.innerHTML = `The model has been switched to <b>Mental Health Sentiment Analysis - Model V1</b>.
                     This model is designed to predict a patient's mental health based on their textual
                     statements, allowing for rapid recognition of critical mental and emotional states. 
                     The current model can predict the following conditions: depression, anxiety, bipolar and normal.
                     
                     Note: please recall that this model is designed for assistive purposes only.
                     `
      responseBody.appendChild(p);
      scrollScreen(p);
      //Perform logic to allow users to summarize documents               
      const buttonListener = () => {
            const responseText = document.createElement("p");
            //Adding a class attribute to each div
            const bodyText = document.createElement("p");
            bodyText.classList.add("responseBox");
            responseText.classList.add("summaryBox");
            //Check if the h2 content is displayed, if it is, remove it,
            if (!(greetingMessage.textContent === "")) {
              //Deactivate 
              greetingMessage.textContent = "";
            }
            if (textBoxArea.value === undefined) {
              throw new Error("The textbox body is empty!");
            }
            const documentMain = textBoxArea.value;
            bodyText.textContent = documentMain;
            addToTextCanva(responseBody, bodyText);
            //Add the scroll option here
            scrollScreen(bodyText);
            loadingIcon();
            //Also send the message to the summarizer via fetch
            postUserSentiment(documentMain, "chatbot_sentiment_post") //Change fetch request to sentiment mode
               .then(() => {
                //If the POST is successful then call get
                 return getUserDocument("sentiment_prediction", "chatbot_sentiment"); //Change fetch request to sentiment mode
               })
               .then((sentiment) => {
                //If get is successful, return the summary
                try {
                  checkLoadingTime(sentiment, responseText);
               } catch (error) {
                 console.log(error);
                 scrollScreen(failureMessage);
              }
               })
               .catch((failureMessage) => {
                console.log(failureMessage);
               });
            // const message = {inputs: bodyText}
            textBoxArea.value = "";
            sendButton.disabled = true;
       }

      currentButtonListener = buttonListener;
      currentKeyupListener = (event) => {
        if (event.code === "Enter") {
          buttonListener();
        }
      };
      sendButton.addEventListener("click", currentButtonListener);
      textBoxArea.addEventListener("keyup", currentKeyupListener);
   }

   const scrollScreen = (element) => {
      responseBody.scrollTo({left:0, top: element.offsetTop, behavior:"smooth"});   
   }

  const  loadingIcon = async () => {
      var loading_icon = document.createElement('img');
      loading_icon.src = "/static/neural/Loading_icon.gif";
      loading_icon.setAttribute("id", "loading_icon");
      loading_icon.width = 80;
      loading_icon.height = 80;
      // responseBody.appendChild(loading_icon);
      addToTextCanva(responseBody, loading_icon);
      scrollScreen(loading_icon);
  }

  const removeLoadingIcon = async () => {
    const loading_icon = document.getElementById("loading_icon");
    responseBody.removeChild(loading_icon);
  }

   const summarizerClassEventListener = function () {
      removeCurrentListeners();
      //Check that the file uploader is none
      if (fileDisplayIcon.style.display === "block") {
        fileDisplayIcon.style.display = "none";
      }
      //Inform user of model switch
      const p = document.createElement("p");
      p.innerHTML = `The model has been switched to <b>Model Summarization - Model V1</b>. Feel free to insert textual documents with a limit of 2000 words,
                     and retrieve the summarized version.`
      responseBody.appendChild(p);
      scrollScreen(p);
      //Perform logic to allow users to summarize documents               
      const buttonListener = () => {
            const responseText = document.createElement("p");
            //Adding a class attribute to each div
            const bodyText = document.createElement("p");
            bodyText.classList.add("responseBox");
            responseText.classList.add("summaryBox");
            //Check if the h2 content is displayed, if it is, remove it,
            if (!(greetingMessage.textContent === "")) {
              //Deactivate 
              greetingMessage.textContent = "";
            }
            if (textBoxArea.value === undefined) {
              throw new Error("The textbox body is empty!");
            }
            const documentMain = textBoxArea.value;
            bodyText.textContent = documentMain;
            addToTextCanva(responseBody, bodyText);
            //Add the scroll option here
            scrollScreen(bodyText);
            loadingIcon();
            //Also send the message to the summarizer via fetch
            postUserDocument(documentMain, "chatbot_request") //Change fetch request to sentiment mode
               .then(() => {
                //If the POST is successful then call get
                 return getUserDocument("summary", "chatbot_summary"); //Change fetch request to sentiment mode
               })
               .then((summary) => {
                try {
                  checkLoadingTime(summary, responseText);
               } catch (error) {
                 console.log(error);
              }
               })
               .catch((failureMessage) => {
                console.log("Error Message: " + failureMessage);
                errorMessage(failureMessage);
               });
            // const message = {inputs: bodyText}
            textBoxArea.value = "";
            sendButton.disabled = true;
       }

      currentButtonListener = buttonListener;
      currentKeyupListener = (event) => {
        if (event.code === "Enter") {
          buttonListener();
        }
      };
      sendButton.addEventListener("click", currentButtonListener);
      textBoxArea.addEventListener("keyup", currentKeyupListener);
   }

   //Adding the event for general summarization    
   //Image classification model
   imageClass.addEventListener("click", imageClassEventListener);
   summarizerClass.addEventListener("click", summarizerClassEventListener);
   textClassification.addEventListener("click", textClassifierEventListener);
   summarizerClassEventListener();

   const errorMessage = (error) => {
        const errorText = document.createElement('p');
        errorText.classList.add("errorMessages");
        errorText.textContent = `There was an error when accessing the response. \nError Type: ${error}`;
        addToTextCanva(responseBody, errorText);
        scrollScreen(errorText);
   }

   const modelSelectionEventHandler = function (modelCategory, responseBody) {
        const uploadButtonEventHandler = (model, userFile) => {
              const successMessage = document.createElement("p");
              successMessage.textContent = "The prediction was successful!";
              const failureMessage = document.createElement("p");
              failureMessage.textContent = "The prediction failed. Please upload again";

              if (userFile) {
                 if (model === "SkinClassifier") {
                  //Send the image to its POST endpoint
                  loadingIcon();
                  postUserImage(userFile, "classification_upload")
                     .then(() => {
                      //Wait for a successful post request, then call get
                      return getUserDocument("prediction", "classification_result");
                     })
                     .then((prediction) => {
                      //Create a neat paragraph element to store the result
                      const parEl = document.createElement("p");
                      const divEl = document.createElement("div");
                      parEl.textContent = prediction;
                      divEl.appendChild(parEl);
                      addToTextCanva(responseBody, divEl);
                      scrollScreen(divEl);
                      removeLoadingIcon();
                     })
                     .catch((error) => {
                       console.log(`Issue: ${error}`);
                       responseBody.appendChild(failureMessage);
                       scrollScreen(failureMessage);
                     });
                }
              else if (model === "PneumoniaClassifier") {
                loadingIcon();
                postUserImage(userFile, "classification_upload_pneumonia")
                     .then(() => {
                      //Wait for a successful post request, then call get
                      return getUserDocument("prediction_pneumonia", "classification_result_pneumonia");
                     })
                     .then((prediction) => {
                      //Create a neat paragraph element to store the result
                      const parEl = document.createElement("p");
                      const divEl = document.createElement("div");
                      parEl.textContent = prediction;
                      divEl.appendChild(parEl);
                      addToTextCanva(responseBody, divEl);
                      scrollScreen(divEl);
                      removeLoadingIcon();
                     })
                     .catch((error) => {
                       console.log(`Issue: ${error}`);
                       responseBody.appendChild(failureMessage);
                       scrollScreen(failureMessage);
                     });
                   }
                } else {
                  throw new Error("The file is empty or corrupted. Please try again");
                }        
            }

            //Create default event handler
            const fetchButtonEventHandler = (model) => { 
              if (defaultEventHandler) {
                fileUploadButton.removeEventListener("change", defaultEventHandler);
              }
            //Append it again  
            defaultEventHandler = () => {
            let userFile = fileUploadButton.files[0];
            if (userFile) {
              uploadButtonEventHandler(model, userFile);
              fileUploadButton.value = "";
              } else {
                console.log("The file is empty or corrupted!");
              }
            };
            fileUploadButton.addEventListener("change", defaultEventHandler);
         }

          const articleEventHandler = (articleId) => {
          const descriptions = [`Model has been switched to <b>Skin Cancer Classifier - Model V1</b>. Please be careful when uploading scans, to ensure accurate predictions.
                            Please note this model is meant for assistive purposes only, and should not be used as a final verdict with respect to the patient.
                            `,
                            `Model has been switched to <b>Pneumonia Classifier - Model V1</b>. Please be careful when uploading scans, to ensure accurate predictions.
                            Please note this model is meant for assistive purposes only, and should not be used as a final verdict with respect to the patient.`]
          console.log(articleId.currentTarget.id);
          let modelId = articleId.currentTarget.id;
          //We must first check the model card id
          // fileUploadButton.disabled = false; //Instead false, we could simply make it visible
          fileDisplayIcon.style.display = "block";
          let model = "";
          //if the id is AT1 - use the skin cancer classifier
          if (modelId === "AT1") {
             //Enable and highlight send button
              fileDisplayIcon.style.display = "block";
              const modelType = document.createElement("p");
              const div = document.createElement("div");
              model = "SkinClassifier";
              //Then add the model description
              modelType.innerHTML = descriptions[0];
              div.appendChild(modelType);
              responseBody.appendChild(div);
              scrollScreen(div);
          }
          else if (modelId === "AT2") {
              fileDisplayIcon.style.display = "block";
              const modelType = document.createElement("p");
              const div = document.createElement("div");
              model = "PneumoniaClassifier";
              //Then add the model description
              modelType.innerHTML = descriptions[1];
              div.appendChild(modelType);
              responseBody.appendChild(div);
              scrollScreen(div);
          }
          fetchButtonEventHandler(model);
         }
       if (modelCategory) {
          //Gather the model id's for each article
          const modelSectionArticles = modelCategory.querySelectorAll("article");
          console.log(modelSectionArticles);
          modelSectionArticles.forEach((article) => {
            //For each article, add an event handler
            console.log(article);
            article.addEventListener("click", articleEventHandler);
          });
         } 
    }
    //When the screen resizes, adjust the selection option
    const windowResizeCheck = function () {
        if (window.innerWidth < 1000) {
                //add margin to the right of the task selector of 30px
                taskSelectionMenu.style.marginRight = "200px";
            } else {
                taskSelectionMenu.style.marginRight = 0;
            }
        }
      windowResizeCheck();
      window.addEventListener("resize", windowResizeCheck);
        
    //Check that the model category section is not undefine
   const classificationService = function(classifierPath, uploadedFile, getPathName, postPath) {
      const loader = document.createElement("div");
        loader.classList.add("loader");
        responseBody.appendChild(loader);
        const userImage = uploadedFile;
        //When it changes, send the image file to the expected HTTP path
        postUserImage(userImage, postPath)
          .then(() => {
              // If post request is successful, then call get
              return getUserDocument(`${getPathName}`, `${classifierPath}`);
          })
          .then((prediction) => {
            //  If prediction is successful show both the image and the prediction
            const divItem = document.createElement("div");
            
            const p = document.createElement("p");
            p.textContent = prediction; //get the predicted result
            divItem.appendChild(p);
            //Add the div to the response body for the user to see
            setTimeout(() => {
              responseBody.removeChild(loader);
              addToTextCanva(responseBody, divItem);
            }, 2000);     
          })
          .catch((error) => {
            console.log(error);
          });
   }
   
   //Add event listeners to the article cards
    const taskSelectionEvent = () => {
      if (taskSelectionMenu.style.display === "block") {
            taskSelectionMenu.style.display = "none"; 
          }
      else if (taskSelectionMenu.style.display === "none") {
          taskSelectionMenu.style.display = "block"; 
      }
    }

   taskSelectionMenu.addEventListener("mouseleave", () => {
       if (taskSelectionMenu.style.display === "block"){
        taskSelectionMenu.style.display = "none"; 
        console.log("unblock");
       } else {
        taskSelectionMenu.style.display = "block";
        console.log("block");
       }  
     });

     menuButton.addEventListener("click", () => {
       taskSelectionEvent();
     });

    function addToTextCanva(parentElement, childElement){
       //This function is designed to add the sent text to the main body
        parentElement.appendChild(childElement);
    }

    // If the text area has a length of text greater than 5 characters allow for the send action
    textBoxArea.addEventListener("input", (e)=>{
       let inputTextLength = textBoxArea.value.length;
       

       if (inputTextLength >= 3) {
        sendButton.disabled = false;
        //Hereafter add an event listener to the button - when clicked, send the text to the screen as a new component
       } else if (inputTextLength < 3){
        sendButton.disabled = true;
       }
    });

    // Create an event listener for the send button, which upon being sent will retrieve the user document from the text area, and
    // send it as a post request to the respective POST location
    const postUserDocument = async function(file, checkpoint) { //Returns a promise
            if (file === undefined) {
                throw new Error("The document is empty!");
            }
            await fetch(`http://localhost:8000/neural/${checkpoint}/`, {
                    method: "POST",
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({"document": file}),                  
            }).then(response => {
              if (response.ok) {
                return response.json();
              }
              throw new Error('Request failed!');
            }, networkError => console.log(networkError.message)   
          ).then(jsonResponse => {
            console.log(jsonResponse);
          })
        } 

         const postUserSentiment = async function(statement, checkpoint) { //Returns a promise
            if (document === undefined) {
                throw new Error("The document is empty!");
            }
                await fetch(`http://localhost:8000/neural/${checkpoint}/`, {
                    method: "POST",
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({"sentiment": statement}),                  
            }).then(response => {
              if (response.ok) {
                return response.json();
              }
              throw new Error('Request failed!');
            }, networkError => console.log(networkError.message)   
          ).then(jsonResponse => {
            console.log(jsonResponse);
          })
        } 
        
      const postUserImage = async function (file, checkpoint) {
        console.log(checkpoint);
           const formData = new FormData();
           formData.append("file", file);

            await fetch(`http://localhost:8000/neural/${checkpoint}/`, {
            method:"POST",
            body: formData
           })
           .then(response => {
            response.json();
              })
           .then (
            success => {console.log(success);
            }
           )
           .catch (
             error => {
              console.log(error);
             }
           )};
          // return the summarized data to the user
        const getUserDocument = async (key, checkpoint) => {
          try {
            const response = await fetch(`http://localhost:8000/neural/${checkpoint}/`);
            if (response.ok) {
              const jsonResponse = await response.json();
              //returns a JavaScript object with the summary
              const userResult = jsonResponse[`${key}`];
              console.log(userResult);
              return userResult;
            }
            throw new Error('Request failed!');
          } catch (error) {
            console.log(error);
          }          
        }
disableSendButton();