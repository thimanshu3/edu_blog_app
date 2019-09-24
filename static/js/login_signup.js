function validatePass(){
    var pass1 = document.getElementById('password').value;
    var passregex = /^(?=.*\d).{6,20}$/;
    if(pass1.match(passregex)){
        document.getElementById('signupButton').disabled = false;
    }
    else{
        alert("Password length must be 6 to 20, should contain at least one digit and one letter");
        document.getElementById('signupButton').disabled = true;
    }
}

function confirmPass(){
    var pass1 = document.getElementById('password').value;
    var pass2 = document.getElementById('confirmpassword').value;
    if(pass1 != pass2){
        alert("Password and Confirm Password should match");
        document.getElementById('signupButton').disabled = true;
    }
    else{
        document.getElementById('signupButton').disabled = false;
    }
}

function checkPassword(){
    var pass1 = document.getElementById('newpassword').value;
    var passregex = /^(?=.*\d).{6,20}$/;
    if(pass1.match(passregex)){
        document.getElementById('changepassbtn').disabled = false;
    }
    else{
        alert("Password length must be 6 to 20, should contain at least one digit and one letter");
        document.getElementById('changepassbtn').disabled = true;
    }
}

function confirmChangePass(){
    var pass1 = document.getElementById('newpassword').value;
    var pass2 = document.getElementById('confirmpassword').value;
    if(pass1 != pass2){
        alert("Password and Confirm Password should match");
        document.getElementById('changepassbtn').disabled=true;
    }
    else{
        document.getElementById('changepassbtn').disabled=false;
    }
}
