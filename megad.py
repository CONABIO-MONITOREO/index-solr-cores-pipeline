from megadetector.detection.run_detector_batch import \
    load_and_run_detector_batch, write_results_to_file
from megadetector.utils import path_utils
import argparse

def main():
    detector_filename = '/LUSTRE/users/promero/md_v5a.0.0.pt'

    parser = argparse.ArgumentParser(description="Especificar parametros")
    parser.add_argument("image_folder", type=str, help="La ubicacion del directorio de las imagenes")
    parser.add_argument("output_file", type=str, help="La ubicacion del archivo de salida")
    parser.add_argument("detector_filename", type=str, nargs='?', default=detector_filename, \
                        help="La ubicacion del archivo de deteccion")
    args = parser.parse_args()
 
    image_folder = args.image_folder
    output_file = args.output_file

    print(image_folder)
    print(output_file)

    if args.detector_filename!=None:
        detector_filename = args.detector_filename
    
    print(detector_filename)

    image_file_names = path_utils.find_images(image_folder,recursive=True)
    results = load_and_run_detector_batch(detector_filename, image_file_names)
    write_results_to_file(results,
                      output_file,
                      relative_path_base=image_folder,
                      detector_file=detector_filename)
    

if __name__ == "__main__":
    main()