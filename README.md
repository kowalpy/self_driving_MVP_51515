# self_driving_MVP_51515
Attempt to make MVP (51515 robot inventor) drive autonomously.

MVP was built according to manual with 3 differences:
- distance sensor attached and connected to port F
- initial angle of front motor set to 90
- unnecessary car body elements removed (for example to make place for distance sensor)

![alt text](https://github.com/kowalpy/self_driving_MVP_51515/blob/main/img/mvp_with_distance_sensor.jpg "Example of MVP with distance sensor")

Directory _src_ contains python file with a self driving program. It tries to make MVP going continously in a room and avoiding colisions. There are few constraints which will never make MVP fully autonomous car:
- lack of back distance sensor; for example when it goes back, controller has no idea about objects behind
- actually also 2 other sensors would be useful at sides
- distance sensor work very well if object is perpendicular to moving direction; if object is at some different angle then it may not work so well

Anyway playing with 51515 is fun and I hope you find my simple program useful. Feel free to improve it via pull requests.

I don't take any responsibility for damage caused by self driving MVP ;-)

