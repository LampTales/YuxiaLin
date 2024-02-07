import os

name_list= {
    '3星结束行动' : 'three_star_end_action',
    '交谈1' : 'talk_1',
    '交谈2' : 'talk_2',
    '交谈3' : 'talk_3',
    '任命助理' : 'assign_assistant',
    '任命队长' : 'assign_leader',
    '作战中1' : 'during_battle_1',
    '作战中2' : 'during_battle_2',
    '作战中3' : 'during_battle_3',
    '作战中4' : 'during_battle_4',
    '信赖提升后交谈1' : 'trust_improve_talk_1',
    '信赖提升后交谈2' : 'trust_improve_talk_2',
    '信赖提升后交谈3' : 'trust_improve_talk_3',
    '信赖触摸' : 'trust_touch',
    '完成高难行动' : 'high_difficulty_action',
    '干员报到' : 'operator_report',
    '戳一下' : 'poke',
    '晋升后交谈1' : 'promotion_talk_1',
    '晋升后交谈2' : 'promotion_talk_2',
    '标题' : 'title',
    '精英化晋升1' : 'elite_promotion_1',
    '精英化晋升2' : 'elite_promotion_2',
    '编入队伍' : 'join_team',
    '行动出发' : 'action_begin',
    '行动失败' : 'action_fail',
    '行动开始' : 'action_start',
    '观看作战记录' : 'watch_battle_record',
    '进驻设施' : 'enter_facility',
    '选中干员1' : 'select_operator_1',
    '选中干员2' : 'select_operator_2',
    '部署1' : 'deploy_1',
    '部署2' : 'deploy_2',
    '问候' : 'greet',
    '闲置' : 'idle',
    '非3星结束行动' : 'non_three_star_end_action',
}

path = 'lin_voice/jp'

def get_file_names_without_extension(dir_path):
    file_names = os.listdir(dir_path)
    file_names_without_extension = [os.path.splitext(file_name)[0] for file_name in file_names]
    return file_names_without_extension


def rename_files(dir_path, name_list):
    file_names = get_file_names_without_extension(dir_path)
    for file_name in file_names:
        if file_name in name_list:
            os.rename(f'{dir_path}/{file_name}.wav', f'{dir_path}/{name_list[file_name]}.wav')
            print(f'{file_name} -> {name_list[file_name]}')
        else:
            print(f'{file_name} not in name_list')


if __name__ == '__main__':
    rename_files(path, name_list)
