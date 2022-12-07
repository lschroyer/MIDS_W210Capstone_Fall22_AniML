**Ivan Wong**

**11/3/22**

**FastAPI Web Server for AniML**

*Environment*
* Login to EC2 Farmlive2 instance
* Create conda environment
   * conda create -c conda-forge --name anymlws_p39 python=3.9

*Run application*
* conda env list
* conda activate anymlws_p39 
* cd /data/fastapi_animl_ws
* Start Unicorn
	 * uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
	 * http://<your_EC2_instance_IP>:8080 
	 * i.e. http://52.52.143.50:8080/
	 
*Files for Detection and Training APIs integration*
* fastapi_animl_ws/app/main.py
* fastapi_animl_ws/app/pages/about.md
* fastapi_animl_ws/app/pages/index.html
* fastapi_animl_ws/app/pages/training.html
* fastapi_animl_ws/static/css/styles.css
* fastapi_animl_ws/static/images/favicon.ico
* fastapi_animl_ws/static/js/app.js
* fastapi_animl_ws/static/js/training.js
* fastapi_animl_ws/templates/base.html
	 
