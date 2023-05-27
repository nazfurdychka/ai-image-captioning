import os

comment_column_name = 'comment'
start_seq_token = 'startseq'
end_seq_token = 'endseq'

path_to_captions_csv = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)), 'sources', 'captions.csv')

team_button_message = 'Team Information'
metrics_button_message = 'Achieved model metrics'
photo_button_message = 'Process photo'
wait_for_photo_command = 'wait_for_photo'


def get_captioning_model_path(model_name):
    return os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)), 'sources',
        model_name)
