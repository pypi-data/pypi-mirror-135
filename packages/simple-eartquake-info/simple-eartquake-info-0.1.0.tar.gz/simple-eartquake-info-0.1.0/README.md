# Simple Eartquake Information
This package will get the simple info of eartquake from BMKG

## HOW TO USE
```
import gempaterkini

if __name__ == "__main__":
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)
```

## HOW IT WORK?
This package will scrape from [BMKG](https://bmkg.go.id)

This package will use BeautifulSoap4 and Request to produce output in the form of JSON that is ready to be used in web or mobile application
