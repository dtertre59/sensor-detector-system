
# WRITE VIDEO


import cv2

def main():
    # Define the window name
    windowname = "Codeloop - Writing A Video"
 
    # Open the video file for reading
    cap = cv2.VideoCapture(0)
 
    # Define the output filename, codec, frame rate, and resolution for the output video
    filename = "data/videos/samples/video.mp4"
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    framerate = 29
    resolution = (640, 480)

    # Create a VideoWriter object for writing the output video
    VideoOutPut = cv2.VideoWriter(filename, codec, framerate, resolution)
 
    # Check if the video capture device is opened successfully
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False
 
    # Loop through the video frames
    while ret:
        # Read the next frame from the video
        ret, frame = cap.read()
 
        # Draw a green circle on the frame
        cv2.circle(frame, (200, 200), 80, (0, 255, 0), -1)

        resized_frame = cv2.resize(frame, resolution)
        # Display the frame in the window
        cv2.imshow(windowname, resized_frame)
        # Write the frame to the output video
        VideoOutPut.write(resized_frame)
 
        
 
        # Check for key press to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
 
    # Destroy all OpenCV windows
    cv2.destroyAllWindows()
 
    # Release the VideoWriter object and video capture device
    VideoOutPut.release()
    cap.release()
 
 
if __name__ == "__main__":
    main()
