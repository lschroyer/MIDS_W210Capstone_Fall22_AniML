<!-- /* Apply this to your `table` element. */ -->
<style type="text/css">
    #page tr, #page th {
        padding: 0; 
        margin: 0;
        }
</style>

<!-- And this to your table's `td` elements. */ -->
<table border="0" align="left"> 
        <tr id="page">
            <th id="page">
                <h1 class="cap">Welcome to AniML. </h1> 
                <h3 class="cap">Computer Vision made easy for automated image processing.</h3>
                <br>
                <font font-family='Poppins', sans-serif; font-size= 1.1em; font-weight= 300; line-height= 1.7em; color= "gray";>
                AniMLs is an easy tool for the rapid creation of computer vision systems for analyzing and filtering<br> a large set of raw images down to images of interest
                </font>
            </th>
            <th id="page">
            <img style='vertical-align:left;' src="static/website_images/animl_logo.png" alt="Logo" width=”500″ height=”600″>
            <font color="white">------</font>
            </th>
        </tr>
</table>
<!-- <div style='vertical-align:middle; display:inline;'>
text text
<h1 class="cap">Welcome to AniMLs. </h1> 
<h1 class="cap">Computer Vision made easy for automated image processing.</h1>
</div> -->

<p><font color="white">------</font></p>

## AniML - Home Page

<html>
<head>
    <title>AniML Detect with YOLOv5</title>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="../static/css/styles.css">
    <link rel="stylesheet" href="../static/css/mystyle.css">
    <link rel="stylesheet" href="../static/css/style3.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
        crossorigin="anonymous">
</head>
</html>

1. <span style="color:black"> **Clean up your dataset**</span>

    Take control of a chaotic dataset by uploading it to the platform - AniML automatically sorts and finds images with objects of interest, which you will later label and use to train a supervised ML model.

2. <span style="color:black"> **Train your own AI vision system**</span>

    Using the filtered images from step 1, add labels detailing the class and location of each object you’re trying to detect. Using the labeled dataset, train your own custom ML model that will automatically detect objects of interest for you.

3. <span style="color:black"> **Use your vision system to find objects and generate insights**</span>

    With your new model, automate away all your previously manual steps! Upload new images and AniML will automatically find images with objects of interest AND generate a comprehensive dashboards of metrics detailing what the model found.

&nbsp;
   
Creators:
Ivan Wong,
Lana Elauria,
Lucas Harvey-Schroyer,
Whit Blodgett

UC Berkeley, School of Information 2022 - Masters of Information and Data Science

<style type="text/css">
            /* Callout box - fixed position at the bottom of the page */
            .callout {
            position: fixed;
            bottom: 35px;
            right: 20px;
            margin-left: 20px;
            max-width: 300px;
            }

            /* Callout header */
            .callout-header {
            padding: 25px 15px;
            background: #555;
            font-size: 30px;
            color: white;
            }

            /* Callout container/body */
            .callout-container {
            padding: 15px;
            background-color: #ccc;
            color: black
            }

            /* Close button */
            .closebtn {
            position: absolute;
            top: 5px;
            right: 15px;
            color: white;
            font-size: 30px;
            cursor: pointer;
            }

            /* Change color on mouse-over */
            .closebtn:hover {
            color: lightgrey;
            }
        </style>
<html>
<div class="callout">
    <div class="callout-header">**Please note**</div>
    <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
    <div class="callout-container">
        <p style="color: black;">For AniML beta testing, please use the following dataset for model 1 filtering, model 2 labeling/training, 
        and model 2 classifications. 
        <br><br>Click the download button to save them locally.
        </p>
    <center>
        <a href="static/images/beta testing dataset.zip" download="beta_testing_files">
        <button type="button">Download beta testing files</button>
        </a>
    </center>
    </div>
</div>
</html>