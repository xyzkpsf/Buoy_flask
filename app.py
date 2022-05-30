from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/big-waves", methods=['GET'])
def getBigWaves():
  args = request.args
  sid = args.get('sid', type=str)
  n = args.get('n', type=int)
  return jsonify(getData(sid, n))


def formateFunc(d):
  return {
      "time": f'{d[0]}-{d[1]}-{d[2]}',
      "height": f'{d[8]}',
    }

def getData(sid, n):
  r = requests.get(f"https://www.ndbc.noaa.gov/data/realtime2/{sid}.txt");
  resText = r.text
  contentArr = resText.split("\n")[2:]
  # split data among space for each data row
  splitedArr = [r.split() for r in contentArr]
  # filter invalid WVHT data rows
  filteredArr = [r for r in splitedArr if len(r) >= 8 and  r[8] != 'MM']
  formatedArr = list(map(formateFunc, filteredArr))
  formatedArr.sort(key = lambda x: x['height'], reverse = True)
  return formatedArr[:n]


if __name__ == '__main__':
  app.run(debug=True)