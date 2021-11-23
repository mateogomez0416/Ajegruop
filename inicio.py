from logging import error
import re
from threading import main_thread
from flask import Flask,render_template, redirect, request, url_for,jsonify
from flask import request, flash



#from mensaje import Mensajes
import yagmail as yagmail
import os
from apps import create_app
from apps.config import Config


if __name__ == "__main__":
    confi=Config()
    app = create_app(confi)
    app.run(debug= True)