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
	 * http://52.52.143.50:8080/
