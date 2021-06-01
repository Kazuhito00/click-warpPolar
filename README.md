# click-warpPolar
3点クリックで円を指定し、極座標変換を行うサンプルプログラムです。<br><br>
<img src="https://user-images.githubusercontent.com/37477845/120346347-4187c800-c336-11eb-8c1b-c5c382ac2f62.gif" width="50%">

# Requirements
* OpenCV 3.4.2 or Later

# Usage
実行方法は以下です。<br>
起動後、マウスで3点をクリックし円を指定してください。<br>
```bash
python click-warpPolar.py
```
<br>
実行時には、以下のオプションが指定可能です。

* --device<br>
カメラデバイス番号の指定<br>
デフォルト：0
* --file<br>
動画ファイルの指定 ※指定時にはカメラデバイスより優先<br>
デフォルト：None
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：640
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：480
* --warp_polar_width<br>
極座標変換後の画像の横幅<br>
デフォルト：500
* --warp_polar_height<br>
極座標変換後の画像の縦幅<br>
デフォルト：150
* --initial_angle<br>
極座標変換後の表示原点を何度ずらすか<br>
デフォルト：-90

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
click-warpPolar is under [Apache v2 license](LICENSE).

