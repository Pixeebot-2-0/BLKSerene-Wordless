# ----------------------------------------------------------------------
# Wordless: Tests - Dependency Parser
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

from tests import wl_test_init
from wordless import wl_dependency_parser
from wordless.wl_dialogs import wl_dialogs_misc

main_global = None

def test_dependency_parser():
    main = wl_test_init.Wl_Test_Main()

    main.settings_custom['dependency_parser']['search_settings']['multi_search_mode'] = True
    main.settings_custom['dependency_parser']['search_settings']['search_terms'] = wl_test_init.SEARCH_TERMS

    for i in range(3):
        # Single file
        if i == 0:
            wl_test_init.select_test_files(main, no_files = [0])
        # Multiple files
        elif i == 1:
            wl_test_init.select_test_files(main, no_files = [1, 2])
        # TTR = 1
        elif i == 2:
            wl_test_init.select_test_files(main, no_files = [3])

        global main_global # pylint: disable=global-statement
        main_global = main

        print(f"Files: {' | '.join(wl_test_init.get_test_file_names(main))}")

        wl_dependency_parser.Wl_Worker_Dependency_Parser(
            main,
            dialog_progress = wl_dialogs_misc.Wl_Dialog_Progress_Process_Data(main),
            update_gui = update_gui
        ).run()

def update_gui(err_msg, results):
    print(err_msg)
    assert not err_msg
    assert results

    file_names_selected = list(main_global.wl_file_area.get_selected_file_names())

    for (
        head, dependent, dependency_relation, dependency_len,
        sentence_display, sentence_search,
        no_sentence, len_sentences, file
    ) in results:
        # Head
        assert head
        # Dependent
        assert dependent
        # Dependency Relation
        assert dependency_relation
        # Dependency Length
        assert isinstance(dependency_len, int)

        # Sentence
        assert all(sentence_display)
        assert all(sentence_search)

        # Sentence No.
        assert no_sentence >= 1
        assert len_sentences >= 1
        # File
        assert file in file_names_selected

if __name__ == '__main__':
    test_dependency_parser()
