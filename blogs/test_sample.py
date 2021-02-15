{% load static %}
{% load tz %}
{% load permission_tags %}

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <link rel="icon" href="{% static 'images/keysight_url.JPG' %}"  sizes="16x16">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- <style>
    .footer {
       position: fixed;
       left: 0;
       bottom: 0;
       width: 100%;
       /* background-color: #1da1ad; */
       color: black;
       text-align: center;
    }
    </style> -->

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <link rel="stylesheet" href="{% static 'css/todo.css' %}">
<meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

<!-- About User icon -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

    <!--High Chart -->

    <script src="https://code.highcharts.com/highcharts.src.js"></script>

    <script src="http://code.highcharts.com/modules/exporting.js"></script>
    <script src="http://code.highcharts.com/modules/offline-exporting.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/export-data.js"></script>
<script src="https://code.highcharts.com/stock/highstock.js"></script>

<script src="https://code.highcharts.com/modules/drilldown.js"></script>
<script src="{% static 'js/todo_orders.js' %}"></script>





    <title>Keysight BI!</title>
  </head>
      <a class="navbar-brand"  href="{% url 'ldapexpiry' %}"> <img src="{% static 'images/keysight-logo.png' %}"  width="100" height="32" ></a>
      <nav class="navbar navbar-expand-lg navbar-light style="background-color: #e3f2fd;" >

        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="{% if nbar == 'ldapexpiry' %}active{% endif %}">
              <a class="nav-link" href="{% url 'ldapexpiry' %}"><strong>App Status </strong><span class="sr-only">(current)</span></a>
            </li>
            <li class="{% if nbar == 'dash' %}active{% endif %}">
              <a class="nav-link" href="{% url 'dashboards' %}"><strong>Dashboards </strong><span class="sr-only">(current)</span></a>
            </li>

            <li class="{% if nbar == 'cred' %}active{% endif %}">
              <a class="nav-link" href="{% url 'applcred' %}"><strong>Credentials </strong><span class="sr-only">(current)</span></a>
            </li>
            <li class="{% if nbar == 'ordlkp' %}active{% endif %}">
              <a class="nav-link" href="{% url 'orders' %}"><strong>Orders Lookup </strong> <span class="sr-only">(current)</span></a>
            </li>
            <li class="{% if nbar == 'rptlink' %}active{% endif %}">
              <a class="nav-link" href="{% url 'reportlink' %}"><strong>Reports </strong> <span class="sr-only">(current)</span></a>
            </li>
            {% if user|can:'add' %}

      <li class="{% if nbar == 'links' %}active{% endif %}">
        <a class="nav-link" href="{% url 'add_load' %}"><strong>Record Data Loads</strong> <span class="sr-only">(current)</span></a>
      </li>
      {% endif %}
      <li class="{% if nbar == 'mecrep' %}active{% endif %}">
        <a class="nav-link" href="{% url 'view_mec_table' %}"><strong>MEC Flash Report </strong> <span class="sr-only">(current)</span></a>
      </li>

      <li class="{% if nbar == 'links' %}active{% endif %}">
        <a class="nav-link" href="{% url 'view_archives_by_date' %}"><strong>MEC Archive</strong> <span class="sr-only">(current)</span></a>
      </li>
      <li class="{% if nbar == 'links' %}active{% endif %}">
        <a class="nav-link" href="{% url 'pword_expiry_calculator' %}"><strong>Password Expiry Tracker</strong> <span class="sr-only">(current)</span></a>
      </li>
      <li class="{% if nbar == 'links' %}active{% endif %}">
        <a class="nav-link" href="{% url 'view_all_loads' %}"><strong>View Loads for this MEC</strong> <span class="sr-only">(current)</span></a>
      </li>

          </ul>

          <div class="dropdown navbar-btn pull-right">
              <button class="btn btn-info dropdown-toggle navbar-btn pull-right" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                {{ user.first_name }}
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
                    <button type="button" class="dropdown-item" data-toggle="modal" data-target="#modal-1">About</button>
                  <button class="dropdown-item" type="button"  onclick="location.href='{% url 'logout_view' %}'">Log out</button>

                </div>
          </div>

                <!-- <a href="{% url 'logout_view' %}" type="button" class="btn btn-default navbar-btn pull-right"><span class="glyphicon glyphicon-log-out"></span>Log out
                </a>
                <a type="button" class="btn btn-default navbar-btn pull-right"><span class="glyphicon glyphicon-user"></span> {{ user.first_name }}
                </a>
                <a type="button" class="btn btn-default navbar-btn pull-right">{{ user.first_name }} <i class="fa fa-bars"></i></button></a> -->


        </div>
      </nav>


<!-- Modal -->
            <div class="modal fade" id="modal-1" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle"><h2><center> BI HeartRate </center></h2></h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    Version 1.6 <br/>
                    Build 23-Feb-2020
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>

                  </div>
                </div>
              </div>
            </div>

<body>

{% block content %}
{% endblock %}



    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>


    <!-- <div class="footer">
      <center>© {% now "Y" %} Copyright:  Keysight BI Team</center>
      <br/>
    <center>Contact Us: <a href="mailto:ccx-bi-coe.pdl-it@keysight.com" target="_top"> ccx-bi-coe.pdl-it@keysight.com</a></center>
      <!-- Version:  1.1 -->
    </div>


  </body>


</html>
