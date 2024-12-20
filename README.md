<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Plate Vision</h3>

  <p align="center">
    Fall 2024 Senior Project at San Jose State University utilizing machine vision to build a parking pass system.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Explanation of Project Structure</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Plate Vision is an innovative parking management system leveraging Raspberry Pi and cloud-based machine learning technologies. The system uses a Raspberry Pi Camera Module 2 to stream live video and detect motion, capturing frames when activity is detected. Captured images are uploaded to AWS S3 and processed using a YOLOv5 object detection model deployed on an Amazon SageMaker real-time endpoint. The model identifies license plates, and Google OCR extracts license plate text for validation against a DynamoDB database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

This project is not meant to be run directly from Github. It is deployed using a hybrid model on a cloud service provider. As such, it is not possible for use directly from this Github repo. However, the full code to the project, as well as the machine learning model artifacts and the results folder from the training have all been provided here.

### Explanation of Project Structure

* `yolov5_license_plate_v13` is the folder containing the trained YOLOv5 model. In the directory, you will find the model weights (`best` and `last`), as well as the options and hyperparameters used in the training in the form of `.yaml` configuration files.
* `model_directory` represents the directory structure that is deployed along with the SageMaker endpoint. It is packaged with the endpoint when it gets deployed and contains the `inference.py` file which tells the endpoint how to perform its inference. It also contains a `requirements.txt` file listing the required Python packages at runtime.
* `results` contain the results from training the YOLOv5 model. It contains all the images, `.csv` files, confusion matrix, labels, and other artifacts from the training used to analyze the model.
* `camera.py` is the script file that is loaded onto the Raspberry Pi Zero 2W to preprocess incoming video streams and upload them onto S3. Variable values have been sanitized.
* `create_realtime_sagemaker.zip` contains the Lambda script to create the real-time SageMaker endpoint. It is only run once on deployment.
* `plate-vision.zip` contains the main Lambda function that performs the workflow of the project.
* `requests_layer.zip` is a layer that is added to the Lambda environment on AWS to allow HTTP requests.
* `project.v1i.yolov5pytorch.zip` contains the dataset, the class files, the labels, and the training images separated into training, validation, and testing sets.


### Installation

1. create an account on Amazon Web Services
2. ensure that model artifacts are uploaded onto S3 in a bucket
3. download, then upload the `create_realtime_sagemaker.zip` file onto the Lambda console
4. verify successful creation of the endpoint
5. download, then upload the `plate-vision.zip` file onto the Lambda console
6. attach roles with adequate permissions onto `plate-vision.zip`
7. download, then upload the `requests_layter.zip` file onto the Lambda console as a layer. Attach the layer to the Lambda function.
8. attach HTTP API Gateway to the main Lambda function
9. create a trigger for the main Lambda function that runs when image gets uploaded onto S3
10. load `camera.py` file onto the Raspberry Pi Zero 2W
11. get API key from Google OCR and use API key credentials in Lambda function
12. set up front end website and ensure that it works with the HTTP API Gateway

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

With the system built and deployed. User interaction will take place on the front-end website. Project should be live, continuously running, and real-time compatible.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the Apache 2.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

David S. Huang - david.sl.huang@gmail.com

Project Link: [https://github.com/daveslh/SJSU-CMPE-195B-Senior-Design-Project-Plate-Vision.git](https://github.com/daveslh/SJSU-CMPE-195B-Senior-Design-Project-Plate-Vision.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The project creators would like to thank Dr. Stas Tiomkin and Dr. Wencen Wu of SJSU for their assistance and guidance in the lifecycle of this project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/daveslh/SJSU-CMPE-195B-Senior-Design-Project-Plate-Vision/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/daveslh/SJSU-CMPE-195B-Senior-Design-Project-Plate-Vision/forks
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/daveslh/SJSU-CMPE-195B-Senior-Design-Project-Plate-Vision/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
