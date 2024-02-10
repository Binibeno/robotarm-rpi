
max_value = 255
max_value_H = 360//2
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection (mask)'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'



# like used in google color picker
def hsv_to_standard(h, s, v):
    # Ensure input values are within the valid range
    h = max(0, min(255, h))
    s = max(0, min(255, s))
    v = max(0, min(255, v))

    # Convert H, S, V to the standard range
    h_standard = (h / 255) * 360
    s_standard = (s / 255) * 100
    v_standard = (v / 255) * 100

    return h_standard, s_standard, v_standard


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
