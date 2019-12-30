from blog_ku import app
from blog_ku import models
import os

port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host='0.0.0.0', port=port)
# if __name__=="__main__":
# 	app.run (debug=True)