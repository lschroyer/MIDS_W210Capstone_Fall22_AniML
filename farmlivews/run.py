from web import app

# Original code
# if __name__ == '__main__':
#    app.run(debug=True)

# Ivan added code 12-26-2020
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888)