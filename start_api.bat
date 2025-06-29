@echo off
set SECRET_KEY=kk39Sy__Md4wbXwSn9fm-uv_I1fu_AT65ir3S_wBtJw
set MVP_API_KEY_SALT=WJ5-hCmlQ1Hwjnu-wVKFBg
set ENVIRONMENT=development
python -m uvicorn master_luciq_api:app --host 0.0.0.0 --port 8000 --reload 