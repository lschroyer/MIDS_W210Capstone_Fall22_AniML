# Contact Information

If you have any questions or suggestions, do not hesitate to reach out!


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
    <textarea id="message" class="input" name="message" rows="7" cols="30"></textarea><br />
    <span id="message_validation" class="error_message"></span> 
  </div>

  <input id="submit_button" name="submit_button" type="submit" value="submit form" />
</form>

<br /><br /><br />

## Response

<textarea id="box" rows="3" cols="30"></textarea>


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