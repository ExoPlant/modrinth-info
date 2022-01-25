import PySimpleGUI as sg
import subprocess as sp
import sys
import requests
import json

version_number = '0.1.0'

def runcmd(cmd, shell=False, check=False):
    return sp.run(cmd, shell=shell, check=check)

def pretty_print(json_file, indentation=4):
    return json.dumps(json_file, indent=indentation)


def main():
    font = ('Arial, 11')
    font_title = ('Arial, 18')
    sg.theme("DarkGrey9")
    main_layout = [
                  [sg.Text('Modrinth Info', font=font)],
                  [sg.Text('Project ID', font=font), sg.InputText()],
                  [sg.Button('Find info', font=font), sg.Button('Cancel', font=font)] 
                  ]
    
    main_window = sg.Window('Modrinth Info', main_layout)
    while True:
        main_event, main_values = main_window.read()
        if main_event == 'Find info':
            r = requests.get(f'https://staging-api.modrinth.com/v2/project/{main_values[0]}')
            response = r.content.decode('UTF-8')
            
            #print(response)
            #print('\n \n \n \n \n \n \n')
            r_json_pretty = pretty_print(r.json())
            print(r_json_pretty)
            print(r.json()['slug'])

            # General

            title = r.json()['title']
            project_id = r.json()['id']
            project_type = r.json()['project_type']
            team_id = r.json()['team']
            short_description = r.json()['description']
            main_description = r.json()['body']
            date_published = r.json()['published']
            last_updated = r.json()['updated']
            project_status = r.json()['status']
            client_side = r.json()['client_side']
            server_side = r.json()['server_side']
            
            # License

            license_id = r.json()['license']['id']
            license_name = r.json()['license']['name']
            license_url = r.json()['license']['url']

            modrinth_data_layout = [
                                   [sg.Text('General', font=font_title)],
                                   [sg.Text(f'Name: {title}', font=font)],
                                   [sg.Text(f'Project ID: {project_id}', font=font)],
                                   [sg.Text(f'Project Type: {project_type}', font=font)],
                                   [sg.Text(f'Team ID: {team_id}', font=font)],
                                   [sg.Text(f'Short Description: {short_description}', font=font)],
                                   [sg.Text(f'Main Description: {main_description}', font=font)],
                                   [sg.Text(f'Date Published: {date_published}', font=font)],
                                   [sg.Text(f'Last Updated: {last_updated}', font=font)],
                                   [sg.Text(f'Project Status: {project_status}', font=font)],
                                   [sg.Text(f'Client Side: {client_side}', font=font)],
                                   [sg.Text(f'Server Side : {server_side}', font=font)],

                                   [sg.Text(f'License', font=font_title)],

                                   [sg.Text(f'ID: {license_id}', font=font)],
                                   [sg.Text(f'Name: {license_name}', font=font)],
                                   [sg.Text(f'URL: {license_url}', font=font)],
                                   [sg.Button('Exit', font=font)] 
                                   ]
            main_window.Hide()
            modrinth_data_window = sg.Window(f'Data for {title}', modrinth_data_layout)
            modrinth_data_event, modrinth_data_values = modrinth_data_window.read()
            if sg.WIN_CLOSED or modrinth_data_event == 'Exit':
                main_window.UnHide()
                modrinth_data_window.close()
            
        if main_event == sg.WIN_CLOSED or main_event == 'Cancel': # if user closes window or clicks cancel
            break

    main_window.close()

if __name__ == "__main__":
    main()