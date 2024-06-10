from megadetector.detection.run_detector_batch import \
    load_and_run_detector_batch, write_results_to_file
from megadetector.utils import path_utils

def main():
    
    image_folder =  '/images/'
    output_file = '/output.json'
    detector_filename = '/model/model.pt'
    
    image_file_names = path_utils.find_images(image_folder, recursive=True)
    results = load_and_run_detector_batch(detector_filename, image_file_names)
    write_results_to_file(results,
                      output_file,
                      relative_path_base=image_folder,
                      detector_file=detector_filename)
    

if __name__ == "__main__":
    main()