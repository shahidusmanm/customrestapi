docker build . --tag=cloudcomputing_scriptbuild:v1
docker run -p 5000:5000 cloudcomputing_scriptbuild:v1