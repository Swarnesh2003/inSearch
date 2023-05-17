function myFunction1() {
    check=0;
    const name=document.getElementById("name").value;
    if(document.getElementById("genm").checked==true)
    {
        const gender=document.getElementById("genm").value;
    }
    else{
        const gender="female";
    }
    const dob= document.getElementById("Birth").value;
    const telp= document.getElementById("tel").value;
    const mail= document.getElementById("email").value;
    const user= document.getElementById("user1").value;
    if(document.getElementById("pw1").value == document.getElementById("pw2").value)
    {
        const pass=document.getElementById("pw1").value;
    }
    else{
        window.alert("Password Doesn't match");
        check=1;
    }
    if(check==0)
    {
        window.alert("signed up")
        const dict_values = {name, gender, dob, telp, mail, user, pass}
        const s = JSON.stringify(dict_values);
        console.log(s)
        $.ajax({
            url:"/test",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s)});
    }
}


  function myFunction() {
    location.replace("index.html");
  }

  /*var myIndex = 0;
  carousel();
  function carousel()
  {
      var i;
      var x = document.getElementsByClassName("mySlides");
      for (i = 0; i < x.length; i++)
      {
          x[i].style.display = "none";  
      }
      myIndex++;
      if (myIndex > x.length) {myIndex = 1}    
      x[myIndex-1].style.display = "block";  
      setTimeout(carousel, 3000); // Change image every 2 seconds
  }*/