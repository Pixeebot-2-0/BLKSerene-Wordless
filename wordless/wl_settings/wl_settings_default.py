# ----------------------------------------------------------------------
# Wordless: Settings - Default Settings
# Copyright (C) 2018-2023  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

import networkx
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDesktopWidget

from wordless.wl_tagsets import (
    wl_tagset_universal,
    wl_tagset_eng_penn_treebank,
    wl_tagset_jpn_unidic,
    wl_tagset_khm_alt,
    wl_tagset_kor_mecab,
    wl_tagset_rus_open_corpora,
    wl_tagset_rus_russian_national_corpus,
    wl_tagset_tha_blackboard,
    wl_tagset_tha_orchid,
    wl_tagset_bod_botok,
    wl_tagset_vie_underthesea,
    wl_tagset_zho_jieba
)
from wordless.wl_utils import wl_misc, wl_paths

_tr = QCoreApplication.translate
is_windows, is_macos, is_linux = wl_misc.check_os()

# The following settings need to be loaded before initialization of the main window
DEFAULT_INTERFACE_SCALING = '100%'

# Font family
if is_windows:
    DEFAULT_FONT_FAMILY = 'Arial'
elif is_macos:
    # SF Pro is the system font on macOS >= 10.11 but is not installed by default
    DEFAULT_FONT_FAMILY = 'Helvetica Neue'
elif is_linux:
    linux_distro = wl_misc.get_linux_distro()

    if linux_distro == 'ubuntu':
        DEFAULT_FONT_FAMILY = 'Ubuntu'
    elif linux_distro == 'debian':
        DEFAULT_FONT_FAMILY = 'DejaVu'

# Font size
if is_windows:
    DEFAULT_FONT_SIZE = 9
elif is_macos:
    DEFAULT_FONT_SIZE = 13
elif is_linux:
    DEFAULT_FONT_SIZE = 11

def init_settings_default(main):
    desktop_widget = QDesktopWidget()

    settings_default = {
        '1st_startup': True,
        'file_area_cur': _tr('init_settings_default', 'Observed Files'),
        'work_area_cur': _tr('init_settings_default', 'Profiler'),

        'menu': {
            'prefs': {
                'display_lang': 'eng_us',
                'layouts': {
                    'central_widget': [main.height() - 210, 210]
                },
                'show_status_bar': True
            },

            'help': {
                'citing': {
                    'select_citation_sys': _tr('init_settings_default', 'APA (7th edition)')
                },

                'donating': {
                    'donating_via': 'PayPal'
                }
            }
        },

        'file_area': {
            'files_open': [],
            'files_open_ref': [],
            'files_closed': [],
            'files_closed_ref': [],

            'dialog_open_files': {
                'auto_detect_encodings': True,
                'auto_detect_langs': True,
                'include_files_in_subfolders': True
            }
        },

        'profiler': {
            'tab': _tr('init_settings_default', 'Counts'),

            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            }
        },

        'concordancer': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'width_left_char': 50,
                'width_left_token': 10,
                'width_left_sentence_seg': 0,
                'width_left_sentence': 0,
                'width_left_para': 0,
                'width_right_char': 50,
                'width_right_token': 10,
                'width_right_sentence_seg': 0,
                'width_right_sentence': 0,
                'width_right_para': 0,
                'width_unit': _tr('init_settings_default', 'Token')
            },

            'table_settings': {
                'show_pct_data': True
            },

            'fig_settings': {
                'sort_results_by': _tr('init_settings_default', 'File')
            },

            'zapping_settings': {
                'zapping': False,
                'replace_keywords_with': 15,
                'placeholder': '_',
                'add_line_nums': True,
                'randomize_outputs': True
            },

            'sort_results': {
                'sorting_rules': [
                    [_tr('init_settings_default', 'File'), _tr('init_settings_default', 'Ascending')],
                    [_tr('init_settings_default', 'Token no.'), _tr('init_settings_default', 'Ascending')]
                ]
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'concordancer_parallel': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'table_settings': {
                'show_pct_data': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'dependency_parser': {
            'token_settings': {
                'punc_marks': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'table_settings': {
                'show_pct_data': True
            },

            'fig_settings': {
                'show_pos_tags': True,
                'show_fine_grained_pos_tags': False,
                'show_lemmas': False,
                'compact_mode': False,
                'show_in_separate_tab': False
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'wordlist_generator': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'generation_settings': {
                'syllabification': True,
                'measure_dispersion': 'juillands_d',
                'measure_adjusted_freq': 'juillands_u'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('init_settings_default', 'Line chart'),
                'sort_by_file': _tr('init_settings_default', 'Total'),
                'use_data': _tr('init_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': _tr('init_settings_default', 'Total'),

                'len_token_min': 1,
                'len_token_min_no_limit': True,
                'len_token_max': 20,
                'len_token_max_no_limit': True,

                'num_syls_min': 1,
                'num_syls_min_no_limit': True,
                'num_syls_max': 20,
                'num_syls_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_min': -100,
                'dispersion_min_no_limit': True,
                'dispersion_max': 100,
                'dispersion_max_no_limit': True,

                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'ngram_generator': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False,

                'search_term_position_min': 1,
                'search_term_position_min_no_limit': True,
                'search_term_position_max': 2,
                'search_term_position_max_no_limit': True
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'ngram_size_sync': False,
                'ngram_size_min': 2,
                'ngram_size_max': 2,
                'allow_skipped_tokens': False,
                'allow_skipped_tokens_num': 1,

                'measure_dispersion': 'juillands_d',
                'measure_adjusted_freq': 'juillands_u'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('init_settings_default', 'Line chart'),
                'sort_by_file': _tr('init_settings_default', 'Total'),
                'use_data': _tr('init_settings_default', 'Frequency'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False,
            },

            'filter_results': {
                'file_to_filter': _tr('init_settings_default', 'Total'),

                'len_ngram_min': 1,
                'len_ngram_min_no_limit': True,
                'len_ngram_max': 20,
                'len_ngram_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'dispersion_min': -100,
                'dispersion_min_no_limit': True,
                'dispersion_max': 100,
                'dispersion_max_no_limit': True,

                'adjusted_freq_min': 0,
                'adjusted_freq_min_no_limit': True,
                'adjusted_freq_max': 1000,
                'adjusted_freq_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'collocation_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_whole_words': False,
                    'match_inflected_forms': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'window_sync': False,
                'window_left': -5,
                'window_right': 5,

                'limit_searching': _tr('init_settings_default', 'None'),

                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'pmi'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_span_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('init_settings_default', 'Line chart'),
                'sort_by_file': _tr('init_settings_default', 'Total'),
                'use_data': _tr('init_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('init_settings_default', 'Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': _tr('init_settings_default', 'Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'colligation_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': True,
                'ignore_tags': False,
                'use_tags': False
            },

            'search_settings': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },

            'context_settings': {
                'incl': {
                    'incl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_inflected_forms': False,
                    'match_whole_words': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                },

                'excl': {
                    'excl': False,

                    'multi_search_mode': False,
                    'search_term': '',
                    'search_terms': [],

                    'match_case': False,
                    'match_inflected_forms': False,
                    'match_whole_words': False,
                    'use_regex': False,
                    'match_without_tags': False,
                    'match_tags': False,

                    'context_window_sync': False,
                    'context_window_left': -5,
                    'context_window_right': 5
                }
            },

            'generation_settings': {
                'window_sync': False,
                'window_left': -5,
                'window_right': 5,

                'limit_searching': _tr('init_settings_default', 'None'),

                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'pmi'
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_span_position': True,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('init_settings_default', 'Line chart'),
                'sort_by_file': _tr('init_settings_default', 'Total'),
                'use_data': _tr('init_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('init_settings_default', 'Total'),

                'len_collocate_min': 1,
                'len_collocate_min_no_limit': True,
                'len_collocate_max': 20,
                'len_collocate_max_no_limit': True,

                'freq_position': _tr('init_settings_default', 'Total'),
                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            },
        },

        'keyword_extractor': {
            'token_settings': {
                'words': True,
                'all_lowercase': True,
                'all_uppercase': True,
                'title_case': True,
                'nums': True,
                'punc_marks': False,

                'treat_as_all_lowercase': False,
                'apply_lemmatization': False,
                'filter_stop_words': False,

                'assign_pos_tags': False,
                'ignore_tags': False,
                'use_tags': False
            },

            'generation_settings': {
                'test_statistical_significance': 'pearsons_chi_squared_test',
                'measure_bayes_factor': 'log_likelihood_ratio_test',
                'measure_effect_size': 'or',
            },

            'table_settings': {
                'show_pct_data': True,
                'show_cum_data': False,
                'show_breakdown_file': True
            },

            'fig_settings': {
                'graph_type': _tr('init_settings_default', 'Line chart'),
                'sort_by_file': _tr('init_settings_default', 'Total'),
                'use_data': _tr('init_settings_default', 'p-value'),
                'use_pct': False,
                'use_cumulative': False,

                'rank_min': 1,
                'rank_min_no_limit': True,
                'rank_max': 50,
                'rank_max_no_limit': False
            },

            'filter_results': {
                'file_to_filter': _tr('init_settings_default', 'Total'),

                'len_keyword_min': 1,
                'len_keyword_min_no_limit': True,
                'len_keyword_max': 20,
                'len_keyword_max_no_limit': True,

                'freq_min': 0,
                'freq_min_no_limit': True,
                'freq_max': 1000,
                'freq_max_no_limit': True,

                'test_stat_min': -100,
                'test_stat_min_no_limit': True,
                'test_stat_max': 100,
                'test_stat_max_no_limit': True,

                'p_val_min': 0,
                'p_val_min_no_limit': True,
                'p_val_max': 0.05,
                'p_val_max_no_limit': True,

                'bayes_factor_min': -100,
                'bayes_factor_min_no_limit': True,
                'bayes_factor_max': 100,
                'bayes_factor_max_no_limit': True,

                'effect_size_min': -100,
                'effect_size_min_no_limit': True,
                'effect_size_max': 100,
                'effect_size_max_no_limit': True,

                'num_files_found_min': 1,
                'num_files_found_min_no_limit': True,
                'num_files_found_max': 100,
                'num_files_found_max_no_limit': True
            },

            'search_results': {
                'multi_search_mode': False,
                'search_term': '',
                'search_terms': [],

                'match_case': False,
                'match_whole_words': False,
                'match_inflected_forms': False,
                'use_regex': False,
                'match_without_tags': False,
                'match_tags': False
            }
        },

        'settings': {
            'node_cur': _tr('init_settings_default', 'General')
        },

        # Settings - General
        'general': {
            'ui_settings': {
                'interface_scaling': DEFAULT_INTERFACE_SCALING,
                'font_family': DEFAULT_FONT_FAMILY,
                'font_size': DEFAULT_FONT_SIZE
            },

            'proxy_settings': {
                'use_proxy': False,
                'address': '',
                'port': '',
                'username': '',
                'password': ''
            },

            'update_settings': {
                'check_updates_on_startup': True
            },

            'misc_settings': {
                'confirm_on_exit': True
            },

            # Settings - General - Import
            'imp': {
                'files': {
                    'default_path': wl_paths.get_normalized_path('.')
                },

                'search_terms': {
                    'default_path': wl_paths.get_normalized_path('.'),
                    'default_encoding': 'utf_8',
                    'detect_encodings': True
                },

                'stop_words': {
                    'default_path': wl_paths.get_normalized_path('.'),
                    'default_encoding': 'utf_8',
                    'detect_encodings': True
                },

                'temp_files': {
                    'default_path': wl_paths.get_normalized_path('imports/'),
                }
            },

            # Settings - General - Export
            'exp': {
                'tables': {
                    'default_path': wl_paths.get_normalized_path('exports/'),
                    'default_type': _tr('init_settings_default', 'Excel workbooks (*.xlsx)'),
                    'default_encoding': 'utf_8'
                },

                'search_terms': {
                    'default_path': wl_paths.get_normalized_path('exports/'),
                    'default_encoding': 'utf_8'
                },

                'stop_words': {
                    'default_path': wl_paths.get_normalized_path('exports/'),
                    'default_encoding': 'utf_8'
                }
            }
        },

        # Settings - Files
        'files': {
            'default_settings': {
                'encoding': 'utf_8',
                'lang': 'eng_us',
                'tokenized': False,
                'tagged': False
            },

            'auto_detection_settings': {
                'num_lines': 100,
                'num_lines_no_limit': False
            },

            'misc_settings': {
                'read_files_in_chunks': 100
            },

            # Settings - Files - Tags
            'tags': {
                'header_tag_settings': [
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Header'), '<teiHeader>', '</teiHeader>']
                ],

                'body_tag_settings': [
                    [_tr('init_settings_default', 'Embedded'), _tr('init_settings_default', 'Part of speech'), '_*', 'N/A'],
                    [_tr('init_settings_default', 'Embedded'), _tr('init_settings_default', 'Part of speech'), '/*', 'N/A'],
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Others'), '<*>', 'N/A']
                ],

                'xml_tag_settings': [
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Paragraph'), '<p>', '</p>'],
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Sentence'), '<s>', '</s>'],
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Word'), '<w>', '</w>'],
                    [_tr('init_settings_default', 'Non-embedded'), _tr('init_settings_default', 'Word'), '<c>', '</c>']
                ]
            }
        },

        # Settings - Sentence Tokenization
        'sentence_tokenization': {
            'sentence_tokenizer_settings': {
                'cat': 'spacy_dependency_parser_cat',
                'zho_cn': 'spacy_dependency_parser_zho',
                'zho_tw': 'spacy_dependency_parser_zho',
                'hrv': 'spacy_dependency_parser_hrv',
                'ces': 'nltk_punkt_ces',
                'dan': 'spacy_dependency_parser_dan',
                'nld': 'spacy_dependency_parser_nld',
                'eng_gb': 'spacy_dependency_parser_eng',
                'eng_us': 'spacy_dependency_parser_eng',
                'est': 'nltk_punkt_est',
                'fin': 'spacy_dependency_parser_fin',
                'fra': 'spacy_dependency_parser_fra',
                'deu_at': 'spacy_dependency_parser_deu',
                'deu_de': 'spacy_dependency_parser_deu',
                'deu_ch': 'spacy_dependency_parser_deu',
                'ell': 'spacy_dependency_parser_ell',
                'ita': 'spacy_dependency_parser_ita',
                'jpn': 'spacy_dependency_parser_jpn',
                'khm': 'khmer_nltk_khm',
                'kor': 'spacy_dependency_parser_kor',
                'lit': 'spacy_dependency_parser_lit',
                'mkd': 'spacy_dependency_parser_mkd',
                'mal': 'nltk_punkt_mal',
                'nob': 'spacy_dependency_parser_nob',
                'nno': 'nltk_punkt_nor',
                'pol': 'spacy_dependency_parser_pol',
                'por_br': 'spacy_dependency_parser_por',
                'por_pt': 'spacy_dependency_parser_por',
                'ron': 'spacy_dependency_parser_ron',
                'rus': 'spacy_dependency_parser_rus',
                'slv': 'spacy_dependency_parser_slv',
                'spa': 'spacy_dependency_parser_spa',
                'swe': 'spacy_dependency_parser_swe',
                'tha': 'pythainlp_crfcut',
                'bod': 'botok_bod',
                'tur': 'nltk_punkt_tur',
                'ukr': 'spacy_dependency_parser_ukr',
                'vie': 'underthesea_vie',

                'other': 'spacy_sentencizer'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Word Tokenization
        'word_tokenization': {
            'word_tokenizer_settings': {
                'afr': 'spacy_afr',
                'sqi': 'spacy_sqi',
                'amh': 'spacy_amh',
                'ara': 'spacy_ara',
                'hye': 'spacy_hye',
                'asm': 'sacremoses_moses',
                'aze': 'spacy_aze',
                'eus': 'spacy_eus',
                'ben': 'sacremoses_moses',
                'bul': 'spacy_bul',
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'hrv': 'spacy_hrv',
                'ces': 'sacremoses_moses',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'est': 'spacy_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'lug': 'spacy_lug',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'grc': 'spacy_grc',
                'ell': 'spacy_ell',
                'guj': 'sacremoses_moses',
                'heb': 'spacy_heb',
                'hin': 'sacremoses_moses',
                'hun': 'sacremoses_moses',
                'isl': 'sacremoses_moses',
                'ind': 'spacy_ind',
                'gle': 'sacremoses_moses',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kan': 'sacremoses_moses',
                'khm': 'khmer_nltk_khm',
                'kor': 'spacy_kor',
                'kir': 'spacy_kir',
                'lat': 'spacy_lat',
                'lav': 'sacremoses_moses',
                'lij': 'spacy_lij',
                'lit': 'spacy_lit',
                'ltz': 'spacy_ltz',
                'mkd': 'spacy_mkd',
                'msa': 'spacy_msa',
                'mal': 'sacremoses_moses',
                'mar': 'sacremoses_moses',
                'mni': 'sacremoses_moses',
                'nep': 'spacy_nep',
                'nob': 'spacy_nob',
                'ori': 'sacremoses_moses',
                'fas': 'nltk_tok_tok',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'pan_guru': 'sacremoses_moses',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'san': 'spacy_san',
                'srp_cyrl': 'spacy_srp',
                'srp_latn': 'spacy_srp',
                'sin': 'spacy_sin',
                'slk': 'sacremoses_moses',
                'slv': 'spacy_slv',
                'dsb': 'spacy_dsb',
                'hsb': 'spacy_hsb',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'tgl': 'spacy_tgl',
                'tgk': 'nltk_tok_tok',
                'tam': 'sacremoses_moses',
                'tat': 'spacy_tat',
                'tel': 'sacremoses_moses',
                'tdt': 'sacremoses_moses',
                'tha': 'pythainlp_max_matching_tcc',
                'bod': 'botok_bod',
                'tir': 'spacy_tir',
                'tsn': 'spacy_tsn',
                'tur': 'spacy_tur',
                'ukr': 'spacy_ukr',
                'urd': 'spacy_urd',
                'vie': 'underthesea_vie',
                'yor': 'spacy_yor',

                'other': 'spacy_eng'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Syllable Tokenization
        'syl_tokenization': {
            'syl_tokenizer_settings': {
                'afr': 'pyphen_afr',
                'sqi': 'pyphen_sqi',
                'bel': 'pyphen_bel',
                'bul': 'pyphen_bul',
                'cat': 'pyphen_cat',
                'hrv': 'pyphen_hrv',
                'ces': 'pyphen_ces',
                'dan': 'pyphen_dan',
                'nld': 'pyphen_nld',
                'eng_gb': 'pyphen_eng_gb',
                'eng_us': 'pyphen_eng_us',
                'epo': 'pyphen_epo',
                'est': 'pyphen_est',
                'fra': 'pyphen_fra',
                'glg': 'pyphen_glg',
                'deu_at': 'pyphen_deu_at',
                'deu_de': 'pyphen_deu_de',
                'deu_ch': 'pyphen_deu_ch',
                'ell': 'pyphen_ell',
                'hun': 'pyphen_hun',
                'isl': 'pyphen_isl',
                'ind': 'pyphen_ind',
                'ita': 'pyphen_ita',
                'lit': 'pyphen_lit',
                'lav': 'pyphen_lav',
                'mon': 'pyphen_mon',
                'nob': 'pyphen_nob',
                'nno': 'pyphen_nno',
                'pol': 'pyphen_pol',
                'por_br': 'pyphen_por_br',
                'por_pt': 'pyphen_por_pt',
                'ron': 'pyphen_ron',
                'rus': 'pyphen_rus',
                'srp_cyrl': 'pyphen_srp_cyrl',
                'srp_latn': 'pyphen_srp_latn',
                'slk': 'pyphen_slk',
                'slv': 'pyphen_slv',
                'spa': 'pyphen_spa',
                'swe': 'pyphen_swe',
                'tel': 'pyphen_tel',
                'tha': 'pythainlp_tha',
                'ukr': 'pyphen_ukr',
                'zul': 'pyphen_zul'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - POS Tagging
        'pos_tagging': {
            'pos_tagger_settings': {
                'pos_taggers': {
                    'cat': 'spacy_cat',
                    'zho_cn': 'spacy_zho',
                    'zho_tw': 'spacy_zho',
                    'hrv': 'spacy_hrv',
                    'dan': 'spacy_dan',
                    'nld': 'spacy_nld',
                    'eng_gb': 'spacy_eng',
                    'eng_us': 'spacy_eng',
                    'fin': 'spacy_fin',
                    'fra': 'spacy_fra',
                    'deu_at': 'spacy_deu',
                    'deu_de': 'spacy_deu',
                    'deu_ch': 'spacy_deu',
                    'ell': 'spacy_ell',
                    'ita': 'spacy_ita',
                    'jpn': 'spacy_jpn',
                    'khm': 'khmer_nltk_khm',
                    'kor': 'spacy_kor',
                    'lit': 'spacy_lit',
                    'mkd': 'spacy_mkd',
                    'nob': 'spacy_nob',
                    'pol': 'spacy_pol',
                    'por_br': 'spacy_por',
                    'por_pt': 'spacy_por',
                    'ron': 'spacy_ron',
                    'rus': 'spacy_rus',
                    'slv': 'spacy_slv',
                    'spa': 'spacy_spa',
                    'swe': 'spacy_swe',
                    'tha': 'pythainlp_perceptron_pud',
                    'bod': 'botok_bod',
                    'ukr': 'spacy_ukr',
                    'vie': 'underthesea_vie'
                },

                'to_universal_pos_tags': False
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            },

            # Settings - POS Tagging - Tagsets
            'tagsets': {
                'preview_settings': {
                    'preview_lang': 'eng_us',
                    'preview_pos_tagger': {}
                },

                'mapping_settings': {
                    'zho_cn': {
                        'jieba_zho': wl_tagset_zho_jieba.MAPPINGS
                    },
                    'zho_tw': {
                        'jieba_zho': wl_tagset_zho_jieba.MAPPINGS
                    },

                    'eng_gb': {
                        'nltk_perceptron_eng': wl_tagset_eng_penn_treebank.MAPPINGS,
                    },
                    'eng_us': {
                        'nltk_perceptron_eng': wl_tagset_eng_penn_treebank.MAPPINGS,
                    },

                    'jpn': {
                        'sudachipy_jpn': wl_tagset_jpn_unidic.MAPPINGS
                    },

                    'khm': {
                        'khmer_nltk_khm': wl_tagset_khm_alt.MAPPINGS
                    },

                    'kor': {
                        'python_mecab_ko_mecab': wl_tagset_kor_mecab.MAPPINGS
                    },

                    'rus': {
                        'nltk_perceptron_rus': wl_tagset_rus_russian_national_corpus.MAPPINGS,
                        'pymorphy3_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                    },

                    'tha': {
                        'pythainlp_perceptron_blackboard': wl_tagset_tha_blackboard.MAPPINGS,
                        'pythainlp_perceptron_orchid': wl_tagset_tha_orchid.MAPPINGS,
                        'pythainlp_perceptron_pud': wl_tagset_universal.MAPPINGS
                    },

                    'bod': {
                        'botok_bod': wl_tagset_bod_botok.MAPPINGS
                    },

                    'ukr': {
                        'pymorphy3_morphological_analyzer': wl_tagset_rus_open_corpora.MAPPINGS
                    },

                    'vie': {
                        'underthesea_vie': wl_tagset_vie_underthesea.MAPPINGS
                    }
                }
            }
        },

        # Settings - Lemmatization
        'lemmatization': {
            'lemmatizer_settings': {
                'sqi': 'simplemma_sqi',
                'hye': 'simplemma_hye',
                'ast': 'simplemma_ast',
                'ben': 'spacy_ben',
                'bul': 'simplemma_bul',
                'cat': 'spacy_cat',
                'hrv': 'spacy_hrv',
                'ces': 'simplemma_ces',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'enm': 'simplemma_enm',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'est': 'simplemma_est',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'glg': 'simplemma_glg',
                'kat': 'simplemma_kat',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'grc': 'spacy_grc',
                'ell': 'spacy_ell',
                'hin': 'simplemma_hin',
                'hun': 'simplemma_hun',
                'isl': 'simplemma_isl',
                'ind': 'simplemma_ind',
                'gle': 'simplemma_gle',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kor': 'spacy_kor',
                'lat': 'simplemma_lat',
                'lav': 'simplemma_lav',
                'lit': 'spacy_lit',
                'ltz': 'simplemma_ltz',
                'mkd': 'spacy_mkd',
                'msa': 'simplemma_msa',
                'glv': 'simplemma_glv',
                'nob': 'spacy_nob',
                'nno': 'simplemma_nno',
                'fas': 'simplemma_fas',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'sme': 'simplemma_sme',
                'gla': 'simplemma_gla',
                'srp_cyrl': 'spacy_srp',
                'srp_latn': 'simplemma_srp_latn',
                'slk': 'simplemma_slk',
                'slv': 'spacy_slv',
                'spa': 'spacy_spa',
                'swa': 'simplemma_swa',
                'swe': 'spacy_swe',
                'tgl': 'simplemma_tgl',
                'bod': 'botok_bod',
                'tur': 'simplemma_tur',
                'ukr': 'spacy_ukr',
                'urd': 'spacy_urd',
                'cym': 'simplemma_cym'
            },

            'preview': {
                'preview_lang': 'eng_us',
                'preview_samples': '',
                'preview_results': ''
            }
        },

        # Settings - Stop Word Lists
        'stop_word_lists': {
            'stop_word_list_settings': {
                'afr': 'stopword_afr',
                'ara': 'stopword_ara',
                'hye': 'stopword_hye',
                'aze': 'nltk_aze',
                'eus': 'stopword_eus',
                'ben': 'stopword_ben',
                'bre': 'stopword_bre',
                'bul': 'stopword_bul',
                'mya': 'stopword_mya',
                'cat': 'stopword_cat',
                'zho_cn': 'stopword_zho_cn',
                'zho_tw': 'stopword_zho_tw',
                'hrv': 'stopword_hrv',
                'ces': 'stopword_ces',
                'dan': 'stopword_dan',
                'nld': 'stopword_nld',
                'eng_gb': 'stopword_eng',
                'eng_us': 'stopword_eng',
                'epo': 'stopword_epo',
                'est': 'stopword_est',
                'fin': 'stopword_fin',
                'fra': 'stopword_fra',
                'glg': 'stopword_glg',
                'deu_at': 'stopword_deu',
                'deu_de': 'stopword_deu',
                'deu_ch': 'stopword_deu',
                'ell': 'stopword_ell',
                'guj': 'stopword_guj',
                'hau': 'stopword_hau',
                'heb': 'stopword_heb',
                'hin': 'stopword_hin',
                'hun': 'stopword_hun',
                'ind': 'stopword_ind',
                'gle': 'stopword_gle',
                'ita': 'stopword_ita',
                'jpn': 'stopword_jpn',
                'kaz': 'nltk_kaz',
                'kor': 'stopword_kor',
                'kur': 'stopword_kur',
                'lat': 'stopword_lat',
                'lav': 'stopword_lav',
                'lit': 'stopword_lit',
                'lgg': 'stopword_lgg',
                'msa': 'stopword_msa',
                'mar': 'stopword_mar',
                'nep': 'nltk_nep',
                'nob': 'stopword_nob',
                'nno': 'nltk_nor',
                'fas': 'stopword_fas',
                'pol': 'stopword_pol',
                'por_br': 'stopword_por_br',
                'por_pt': 'stopword_por_pt',
                'pan_guru': 'stopword_pan_guru',
                'ron': 'stopword_ron',
                'rus': 'stopword_rus',
                'slk': 'stopword_slk',
                'slv': 'stopword_slv',
                'som': 'stopword_som',
                'sot': 'stopword_sot',
                'spa': 'stopword_spa',
                'swa': 'stopword_swa',
                'swe': 'stopword_swe',
                'tgl': 'stopword_tgl',
                'tgk': 'nltk_tgk',
                'tha': 'pythainlp_tha',
                'tur': 'stopword_tur',
                'ukr': 'stopword_ukr',
                'urd': 'stopword_urd',
                'vie': 'stopword_vie',
                'yor': 'stopword_yor',
                'zul': 'stopword_zul',

                'other': 'custom'
            },

            'custom_lists': {},

            'preview': {
                'preview_lang': 'eng_us'
            }
        },

        # Settings - Dependency Parsing
        'dependency_parsing': {
            'dependency_parser_settings': {
                'cat': 'spacy_cat',
                'zho_cn': 'spacy_zho',
                'zho_tw': 'spacy_zho',
                'hrv': 'spacy_hrv',
                'dan': 'spacy_dan',
                'nld': 'spacy_nld',
                'eng_gb': 'spacy_eng',
                'eng_us': 'spacy_eng',
                'fin': 'spacy_fin',
                'fra': 'spacy_fra',
                'deu_at': 'spacy_deu',
                'deu_de': 'spacy_deu',
                'deu_ch': 'spacy_deu',
                'ell': 'spacy_ell',
                'ita': 'spacy_ita',
                'jpn': 'spacy_jpn',
                'kor': 'spacy_kor',
                'lit': 'spacy_lit',
                'mkd': 'spacy_mkd',
                'nob': 'spacy_nob',
                'pol': 'spacy_pol',
                'por_br': 'spacy_por',
                'por_pt': 'spacy_por',
                'ron': 'spacy_ron',
                'rus': 'spacy_rus',
                'slv': 'spacy_slv',
                'spa': 'spacy_spa',
                'swe': 'spacy_swe',
                'ukr': 'spacy_ukr'
            },

            'preview': {
                'preview_lang': 'eng_us',

                'preview_settings': {
                    'show_pos_tags': True,
                    'show_fine_grained_pos_tags': False,
                    'show_lemmas': False,
                    'collapse_punc_marks': True,
                    'compact_mode': False,
                    'show_in_separate_tab': False
                },

                'preview_samples': ''
            }
        },

        # Settings - Tables
        'tables': {
            'rank_settings': {
                'continue_numbering_after_ties': False
            },

            'precision_settings': {
                'precision_decimals': 3,
                'precision_pcts': 3,
                'precision_p_vals': 5
            },

            # Settings - Tables - Profiler
            'profiler': {
                'general_settings': {
                    'num_tokens_section_sttr': 1000
                }
            },

            # Settings - Tables - Concordancer
            'concordancer': {
                'sorting_settings': {
                    'highlight_colors': {
                        'lvl_1': '#FF0000', # Red
                        'lvl_2': '#C2691D', # Orange
                        'lvl_3': '#CBBE00', # Yellow
                        'lvl_4': '#3F864C', # Green
                        'lvl_5': '#264E8C', # Blue
                        'lvl_6': '#491D76', # Purple
                    }
                }
            },

            # Settings - Tables - Parallel Concordancer
            'parallel_concordancer': {
                'color_settings': {
                    'search_term_color': '#FF0000' # Red
                }
            }
        },

        # Settings - Measures
        'measures': {
            # Settings - Measures - Readability
            'readability': {
                'bormuths_gp': {
                    'cloze_criterion_score': 35
                },

                'colemans_readability_formula': {
                    'variant': '2'
                },

                're': {
                    'variant_nld': 'Douma',
                    'variant_spa': 'Fernández Huerta'
                },

                'wstf': {
                    'variant': '1'
                }
            },

            # Settings - Measures - Dispersion
            'dispersion': {
                'general_settings': {
                    'num_sub_sections': 5
                },

                'griess_dp': {
                    'apply_normalization': True
                }
            },

            # Settings - Measures - Adjusted Frequency
            'adjusted_freq': {
                'general_settings': {
                    'num_sub_sections': 5
                }
            },

            # Settings - Measures - Statistical Significance
            'statistical_significance': {
                'fishers_exact_test': {
                    'direction': _tr('init_settings_default', 'Two-tailed')
                },

                'log_likelihood_ratio_test': {
                    'apply_correction': False
                },

                'mann_whitney_u_test': {
                    'num_sub_sections': 5,
                    'use_data': _tr('init_settings_default', 'Relative frequency'),
                    'direction': _tr('init_settings_default', 'Two-tailed'),
                    'apply_correction': True
                },

                'pearsons_chi_squared_test': {
                    'apply_correction': False
                },

                'students_t_test_1_sample': {
                    'direction': _tr('init_settings_default', 'Two-tailed')
                },

                'students_t_test_2_sample': {
                    'num_sub_sections': 5,
                    'use_data': _tr('init_settings_default', 'Relative frequency'),
                    'direction': _tr('init_settings_default', 'Two-tailed')
                },

                'welchs_t_test': {
                    'num_sub_sections': 5,
                    'use_data': _tr('init_settings_default', 'Relative frequency'),
                    'direction': _tr('init_settings_default', 'Two-tailed')
                },

                'z_score': {
                    'direction': _tr('init_settings_default', 'Two-tailed')
                },

                'z_score_berry_rogghe': {
                    'direction': _tr('init_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Bayes Factor
            'bayes_factor': {
                'log_likelihood_ratio_test': {
                    'apply_correction': False
                },

                'students_t_test_2_sample': {
                    'num_sub_sections': 5,
                    'use_data': _tr('init_settings_default', 'Relative frequency'),
                    'direction': _tr('init_settings_default', 'Two-tailed')
                }
            },

            # Settings - Measures - Effect Size
            'effect_size': {
                'kilgarriffs_ratio': {
                    'smoothing_param': 1.00
                }
            }
        },

        # Settings - Figures
        'figs': {
            # Settings - Figures - Line Charts
            'line_charts': {
                'general_settings': {
                    'font': DEFAULT_FONT_FAMILY
                }
            },

            # Settings - Figures - Word Clouds
            'word_clouds': {
                'font_settings': {
                    'font': 'GNU Unifont',
                    'font_path': '',

                    'font_size_min': 4,
                    'font_size_max': desktop_widget.height(),
                    # Auto
                    'relative_scaling': -0.01,

                    'font_color': _tr('init_settings_default', 'Colormap'),
                    'font_color_monochrome': '#000000',
                    'font_color_colormap': 'viridis'
                },

                'bg_settings': {
                    'bg_color': '#FFFFFF',
                    'bg_color_transparent': False
                },

                'mask_settings': {
                    'mask_settings': False,
                    'mask_path': '',
                    'contour_width': 1,
                    'contour_color': '#000000'
                },

                'advanced_settings': {
                    'prefer_hor': 90,
                    'allow_repeated_words': False
                }
            },

            # Settings - Figures - Network Graphs
            'network_graphs': {
                'node_settings': {
                    'node_shape': 'o',
                    'node_size': 800,
                    'node_color': '#5C88C5',
                    'node_opacity': 1.0
                },

                'node_label_settings': {
                    'label_font': DEFAULT_FONT_FAMILY,
                    'label_font_size': DEFAULT_FONT_SIZE,
                    'label_font_weight': 400,
                    'label_font_color': '#000000',
                    'label_opacity': 1.0
                },

                'edge_settings': {
                    'connection_style': 'arc3',
                    'edge_width_min': .1,
                    'edge_width_max': 3,
                    'edge_style': 'solid',
                    'edge_color': '#000000',
                    'edge_opacity': 1.0,
                    'arrow_style': '-|>',
                    'arrow_size': 10
                },

                'edge_label_settings': {
                    'label_position': .5,
                    'rotate_labels': True,
                    'label_font': DEFAULT_FONT_FAMILY,
                    'label_font_size': DEFAULT_FONT_SIZE,
                    'label_font_weight': 400,
                    'label_font_color': '#000000',
                    'label_opacity': 1.0
                },

                'advanced_settings': {
                    'layout': networkx.spring_layout
                }
            }
        }
    }

    # Tagsets
    settings_default['pos_tagging']['tagsets']['preview_settings']['preview_pos_tagger'] = settings_default['pos_tagging']['pos_tagger_settings']['pos_taggers']

    # Custom stop word lists
    for lang in settings_default['stop_word_lists']['stop_word_list_settings']:
        settings_default['stop_word_lists']['custom_lists'][lang] = []

    return settings_default
