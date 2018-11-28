if [ "$1" == "screen" ]; then
    ffmpeg -y -f alsa -i hw:0 -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0+0,0 -c:v libx264 -pix_fmt yuv420p -qp 0 -preset ultrafast ~/Videos/doing/$(date +%F_%A_at_%H:%M:%S).mp4

elif [ "$1" == "me" ]; then
    ffmpeg -hide_banner -loglevel info -thread_queue_size 512 -y -f alsa -i hw:0 -itsoffset -1.266 -thread_queue_size 512 -f x11grab -video_size 1920x1080 -i ":0.0" -thread_queue_size 512 -f v4l2 -video_size 320x240 -i "/dev/video0" -c:v libx264 -crf 30 -preset ultrafast -filter_complex '[2:v]hflip[2:v]; [2:v]eq=brightness=0.04:saturation=0.7[2:v]; [1:v][2:v] overlay=W-w-10:H-h-10' -threads 0 ~/Videos/doing/$(date +%F_%A_at_%H:%M:%S).mp4

elif [ "$1" == "" ]; then
    echo "face
screen
me"
    ffplay -window_title "yingshaoxo" -vf hflip /dev/video0

fi

