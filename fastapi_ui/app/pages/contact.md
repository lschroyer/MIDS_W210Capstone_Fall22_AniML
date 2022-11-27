# Contact Information

If you have any questions or suggestions, do not hesitate to reach out!

<html>
<head>
    <title>AniML Filtering Empty Images</title>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="../static/css/styles.css">
    <link rel="stylesheet" href="../static/css/mystyle.css">
    <link rel="stylesheet" href="../static/css/style3.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
        crossorigin="anonymous">
<h2> AniML - Contact </h2>
</head>
</html>


<form id="contact_form" action="/page/contact/submit" method="POST" enctype="multipart/form-data">
  
  <div style="display:flex; flex-direction: row; justify-content: left; align-items: center">
    <label class="required" for="name">Your name:</label><br />
    &nbsp&nbsp
    <input id="name" class="input" name="name" type="text" value="" size="30" /><br />
    <span id="name_validation" class="error_message"></span>
  </div>
  
  <div style="display:flex; flex-direction: row; justify-content: left; align-items: center">
    <label class="required" for="email">Your email:</label><br />
    &nbsp &nbsp
    <input id="email" class="input" name="email" type="text" value="" size="30" /><br />
    <span id="email_validation" class="error_message"></span>
  </div>
  </br>

  <div cstyle="display:flex; flex-direction: row; justify-content: left; align-items: center">
    <label class="required" for="message">Your message:</label><br />
    <textarea id="message" class="input" name="message" rows="7" cols="30" 
    style="border:solid 1px black;"></textarea><br />
    <span id="message_validation" class="error_message"></span> 
  </div>

  <input id="submit_button" name="submit_button" type="submit" value="submit form" />
</form>

<br /><br />

### Response

<textarea id="box" rows="3" cols="30" style="border:solid 1px black;"></textarea>


<script>
    const box = document.getElementById("box");

    contact_form.onsubmit = async (e) => {
      e.preventDefault();

      let res = await fetch("/page/contact/submit", {
        method: "POST",
        body: new FormData(contact_form),
      });

      if (res.ok) {
        let result = await res.text();
        box.innerHTML = result;
      } else {
        box.innerHTML = `Response error: ${res.status}`;
      };
    };
  </script>