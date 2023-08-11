# ----------------------------------------------------------------------
# Wordless: NLP - Dependency parsing
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

import os
import shutil
import subprocess
import webbrowser

from PyQt5.QtCore import QCoreApplication
import spacy

from wordless.wl_checks import wl_checks_misc
from wordless.wl_dialogs import wl_msg_boxes
from wordless.wl_nlp import wl_matching, wl_nlp_utils
from wordless.wl_utils import wl_conversion, wl_misc, wl_paths

_tr = QCoreApplication.translate

is_windows, is_macos, is_linux = wl_misc.check_os()

def wl_dependency_parse(main, inputs, lang, dependency_parser = 'default', tagged = False):
    if dependency_parser == 'default':
        dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

    wl_nlp_utils.init_dependency_parsers(main, lang, dependency_parser)

    if isinstance(inputs, str):
        dependencies = wl_dependency_parse_text(main, inputs, lang, dependency_parser)
    else:
        dependencies = wl_dependency_parse_tokens(main, inputs, lang, dependency_parser, tagged)

    return dependencies

def wl_dependency_parse_text(main, inputs, lang, dependency_parser):
    dependencies = []

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            for doc in nlp.pipe(inputs.splitlines()):
                dependencies.extend([
                    (token.text, token.head.text, token.dep_, token.head.i - token.i)
                    for token in doc
                ])

    return dependencies

def wl_dependency_parse_tokens(main, inputs, lang, dependency_parser, tagged):
    dependencies = []

    if tagged:
        inputs, tags = wl_matching.split_tokens_tags(main, inputs)

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']
            if nlp.has_pipe(pipeline)
        ]):
            docs = []
            lens_docs = []

            for tokens in wl_nlp_utils.split_token_list(main, inputs, dependency_parser):
                docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens)))

                # Record length of each section
                if tagged:
                    lens_docs.append(len(tokens))

            for i, doc in enumerate(nlp.pipe(docs)):
                if tagged:
                    for token in doc:
                        # Put back tokens and tags
                        i_tag = sum(lens_docs[:i]) + token.i
                        i_tag_head = sum(lens_docs[:i]) + token.head.i

                        dependencies.append((
                            token.text + tags[i_tag], token.head.text + tags[i_tag_head], token.dep_, token.head.i - token.i
                        ))
                else:
                    dependencies.extend([
                        (token.text, token.head.text, token.dep_, token.head.i - token.i)
                        for token in doc
                    ])

    return dependencies

def wl_dependency_parse_fig(
    main, inputs,
    lang, dependency_parser = 'default', tagged = False,
    show_pos_tags = True, show_fine_grained_pos_tags = False,
    show_lemmas = False, collapse_punc_marks = True, compact_mode = False,
    show_in_separate_tab = False
):
    if dependency_parser == 'default':
        dependency_parser = main.settings_custom['dependency_parsing']['dependency_parser_settings'][lang]

    wl_nlp_utils.init_dependency_parsers(main, lang, dependency_parser)

    if isinstance(inputs, str):
        htmls = wl_dependency_parse_fig_text(
            main, inputs,
            lang, dependency_parser,
            show_pos_tags, show_fine_grained_pos_tags,
            show_lemmas, collapse_punc_marks, compact_mode,
            show_in_separate_tab
        )
    else:
        htmls = wl_dependency_parse_fig_tokens(
            main, inputs,
            lang, dependency_parser, tagged,
            show_pos_tags, show_fine_grained_pos_tags,
            show_lemmas, collapse_punc_marks, compact_mode,
            show_in_separate_tab
        )

    return htmls

def _get_pipelines_disabled(show_pos_tags, show_lemmas):
    if show_pos_tags and show_lemmas:
        pipelines_disabled = ['senter', 'sentencizer']
    elif show_pos_tags and not show_lemmas:
        pipelines_disabled = ['lemmatizer', 'senter', 'sentencizer']
    elif not show_pos_tags and show_lemmas:
        pipelines_disabled = ['senter', 'sentencizer']
    elif not show_pos_tags and not show_lemmas:
        pipelines_disabled = ['tagger', 'morphologizer', 'lemmatizer', 'attribute_ruler', 'senter', 'sentencizer']

    return pipelines_disabled

def wl_dependency_parse_fig_text(
    main, inputs,
    lang, dependency_parser,
    show_pos_tags, show_fine_grained_pos_tags,
    show_lemmas, collapse_punc_marks, compact_mode,
    show_in_separate_tab
):
    htmls = []

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in _get_pipelines_disabled(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        ]):
            if show_in_separate_tab:
                for doc in nlp.pipe(inputs.splitlines()):
                    for sentence in doc.sents:
                        htmls.append(spacy.displacy.render(
                            sentence,
                            style = 'dep',
                            minify = True,
                            options = {
                                'fine_grained': show_fine_grained_pos_tags,
                                'add_lemma': show_lemmas,
                                'collapse_punct': collapse_punc_marks,
                                'compact': compact_mode
                            }
                        ))
            else:
                sentences = [
                    sentence
                    for doc in nlp.pipe(inputs.splitlines())
                    for sentence in doc.sents
                ]

                htmls.append(spacy.displacy.render(
                    sentences,
                    style = 'dep',
                    minify = True,
                    options = {
                        'fine_grained': show_fine_grained_pos_tags,
                        'add_lemma': show_lemmas,
                        'collapse_punct': collapse_punc_marks,
                        'compact': compact_mode
                    }
                ))

    return htmls

def wl_dependency_parse_fig_tokens(
    main, inputs,
    lang, dependency_parser, tagged,
    show_pos_tags, show_fine_grained_pos_tags,
    show_lemmas, collapse_punc_marks, compact_mode,
    show_in_separate_tab
):
    htmls = []

    if tagged:
        inputs, tags = wl_matching.split_tokens_tags(main, inputs)

    # spaCy
    if dependency_parser.startswith('spacy_'):
        lang = wl_conversion.remove_lang_code_suffixes(main, lang)
        nlp = main.__dict__[f'spacy_nlp_{lang}']

        with nlp.select_pipes(disable = [
            pipeline
            for pipeline in _get_pipelines_disabled(show_pos_tags, show_lemmas)
            if nlp.has_pipe(pipeline)
        ]):
            docs = []
            lens_docs = []

            for tokens in wl_nlp_utils.split_token_list(main, inputs, dependency_parser):
                docs.append(spacy.tokens.Doc(nlp.vocab, words = tokens, spaces = [False] * len(tokens)))

                # Record length of each section
                if tagged:
                    lens_docs.append(len(tokens))

            options = {
                'fine_grained': show_fine_grained_pos_tags,
                'add_lemma': show_lemmas,
                'collapse_punct': collapse_punc_marks,
                'compact': compact_mode
            }

            if show_in_separate_tab:
                for i_doc, doc in enumerate(nlp.pipe(docs)):
                    for sentence in doc.sents:
                        # Put back tokens and tags
                        displacy_dict = spacy.displacy.parse_deps(sentence.as_doc(), options = options)

                        for token, word in zip(sentence, displacy_dict['words']):
                            i_tag = sum(lens_docs[:i_doc]) + token.i

                            word['text'] += tags[i_tag]

                        htmls.append(spacy.displacy.render(
                            displacy_dict,
                            style = 'dep',
                            minify = True,
                            options = options,
                            manual = True
                        ))
            else:
                sentences = []

                for i_doc, doc in enumerate(nlp.pipe(docs)):
                    for sentence in doc.sents:
                        # Put back tokens and tags
                        displacy_dict = spacy.displacy.parse_deps(sentence.as_doc(), options = options)

                        for token, word in zip(sentence, displacy_dict['words']):
                            i_tag = sum(lens_docs[:i_doc]) + token.i

                            word['text'] += tags[i_tag]

                        sentences.append(displacy_dict)

                htmls.append(spacy.displacy.render(
                    sentences,
                    style = 'dep',
                    minify = True,
                    options = options,
                    manual = True
                ))

    return htmls

def wl_show_dependency_graphs(main, htmls, show_in_separate_tab):
    DIR_PATH = 'exports/_dependency_parsing_figs'

    # Clean cache
    if os.path.exists(DIR_PATH):
        shutil.rmtree(DIR_PATH)

    # Inform users of figures' save location in case the browser does not start successfully
    wl_msg_boxes.Wl_Msg_Box_Info(
        main,
        title = _tr('wl_dependency_parsing', 'Dependency Graphs Generated Successfully'),
        text = _tr('wl_dependency_parsing', '''
            <div>Dependency graphs has been successfully generated and exported under folder: {}</div>

            <div>If the figures are not displayed automatically, you may try opening them manually using web browsers or image viewers installed on your computer, or save copies of them in other locations for later use.</div>
        ''').format(wl_paths.get_normalized_path(DIR_PATH))
    ).open()

    fig_dir = wl_checks_misc.check_dir(DIR_PATH)

    # Change the owner of the figure folder to user on Linux so that figures could be opened with browsers
    if is_linux:
        wl_misc.change_file_owner_to_user(fig_dir)

    if show_in_separate_tab:
        for html in htmls:
            fig_path = wl_checks_misc.check_new_path(os.path.join(fig_dir, 'fig.svg'))
            fig_path = wl_paths.get_normalized_path(fig_path)

            with open(fig_path, 'w', encoding = 'utf_8') as f:
                f.write(html)

            if is_windows or is_macos:
                webbrowser.open(f'file://{fig_path}')
            elif is_linux:
                # Change the owner of the figure file to user on Linux so that the figure could be opened with browsers
                wl_misc.change_file_owner_to_user(fig_path)

                subprocess.Popen(['xdg-open', f'file://{fig_path}']) # pylint: disable=consider-using-with
    else:
        fig_path = wl_checks_misc.check_new_path(os.path.join(fig_dir, 'fig.html'))
        fig_path = wl_paths.get_normalized_path(fig_path)

        with open(fig_path, 'w', encoding = 'utf_8') as f:
            f.write('\n'.join(htmls))

        if is_windows or is_macos:
            webbrowser.open(f'file://{fig_path}')
        elif is_linux:
            # Change the owner of the figure file to user on Linux so that the figure could be opened with browsers
            wl_misc.change_file_owner_to_user(fig_path)

            subprocess.Popen(['xdg-open', f'file://{fig_path}']) # pylint: disable=consider-using-with
