from langchain.document_loaders import UnstructuredURLLoader

urls = [
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/",
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/admissions/",
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/student-life/",
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/academics/",
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/tuition-and-aid/",
    "https://www.collegeconfidential.com/colleges/university-of-missouri-kansas-city/faq/"
]

loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

print(data)