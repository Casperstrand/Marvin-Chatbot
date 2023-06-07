//This is the script that ties the HTML to python program

const getReply = () => {
    //This sets the value of the #textInput as a constant.
    const userInput = $("#textInput").val()
    //And this sets the sets that value as a HTML object
    const userHTML = `<div class="userText"><span>${userInput}</span></div>`
    //Here it connects the python via the route "/get" and sends the variable 'msg'
    //and gets the return back and sets it as 'data' and creates a HTML object with
    //the data.
    $.get("/get", {msg: userInput}).done(data => {
        const botReply = `<div class="botReply"><span>${data}</span></div>`
        //Then it appends both the HTML object to another HTML object called chatbox.
        $("#chatBox").append(userHTML, '<br><br>', botReply)
    })}
//This listens to a specific keypress for the code to run. The keycode I have chosen
//here is the enter key. When this is pressed it runs the function getReply(), clears
//the input and scrolls to the bottom of the object.
$(document).ready(function () {
    $("#textInput").keypress(function (e) {
        if (e.keyCode === 13) {
            getReply()
            $("#textInput").val('')
            $("html, #chatBox").animate({
                scrollTop: ($(document)).height()
            },1000)
        }
    })
    //Since the text input has a value set this function clears it when you press
    //it with the mouse.
    $("#textInput").click(function (){
        $("#textInput").val('')
    })
})