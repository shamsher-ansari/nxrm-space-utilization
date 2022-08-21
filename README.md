## Nexus Repository Space Utilization Report

This script can be used to generate Nexus Repository manager space utilization report, Which can help us to clean up/optimize space utilization.
You can get a detailed report which shows various the contents like Repository Name, Blob Name, with size in MB etc. It is also possible to filter out the output based on criterias like Blob Storage Name, Repository Name, Blob Name, Size, Content type, Created By, Creation Time & Created By IP.

## Quick Start

```
git clone https://github.com/shamsher-ansari/nxrm-space-utilization.git
```
```
cd nxrm-space-utilization/Main
```
```
python run.py #Please run with a user who have access to read Nexus blob storage.
```

<strong> Above should display below output: </strong>

<!-- logo -->
<p align="center">
  <img src="output_report.PNG">
</p>

## History - The Need

I was try to get some method to find out the Nexus repository space utilization stats by Repository name, Blob Name, Content type, Date/Time, Created By, etc. But couldn't find the one. At last I prepared this script and I am sharing the same to help out the community. Please note that this is an open source script please refer the License in the repository. Looking forward to add new features in this script.

## Requirements

* Python 2.x
* Nexus Repository with blob storage of course.
* Linux 

## Tested

On CentOS 7 with Python 2.7.5 and Nexus 3.40.1, You may be wondering why I choose Python 2 instead of Python 3. The reason this that the servers I am working on are mostly CentOS 7, Which by default features Python 2 installed and I wanted to keep the requirments as minimal as possible.

## 💙 Contributing

Have a suggestion? Improvement?

Found a Bug ? Create an Issue.

<br/>




## 💖 Like this project ?

Leave a ⭐ If you think this project is cool.

[Share with the world](https://github.com/shamsher-ansari/nxrm-space-utilization) ✨

<br/>




## 👨‍💻 Author

### Shamsher Ansari

shamsher.ansari5637@gmail.com

<br/>




## 🍁 Licence

**MIT**
