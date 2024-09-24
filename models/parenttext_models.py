from rpft.parsers.creation.datarowmodel import DataRowModel
from rpft.parsers.common.rowparser import ParserModel
from parenttext_pipeline.models.parenttext_models import *
from typing import List

class VMCGameModel(DataRowModel):
    title: str = ''
    references: str = ''
    statement_msg_list: List[str] = []
    statement_image: str = ''
    further_instructions_msg_list: List[str] = []
    strategy_tips_mgs_list: List[str] = []
    about: str = '' 

class VMCFunFactModel(DataRowModel):
    references: str = '' 
    statement_msg_list: List[str] = []
    statement_image: str = '' 
    hint_msg_list: List[str] = []
    explanation_msg_list: List[str] = []
    about_msg_list: List[str] = []				

class VMCPuzzleModel(DataRowModel):
    title: str = ''
    references: str = ''
    about: str = ''
    statement: str = ''
    statement_image: str = '' 
    correct_answer: str = '' 
    hint: str = ''
    explanation: str = '' 
    explanation_image: str = ''
    extension1_statement: str = ''
    extension1_statement_image: str = ''
    extension1_correct_answer: str = ''
    extension1_hint: str = ''
    extension1_explanation: str = ''
    extension1_explanation_image: str = ''
    extension2_statement: str = ''
    extension2_statement_image: str = ''
    extension2_correct_answer: str = ''
    extension2_hint: str = ''
    extension2_explanation: str = ''
    extension2_explanation_image: str = ''					