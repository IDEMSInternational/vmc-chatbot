# Data sources, IDs of Google Sheets where the core date is stored.
# Specific for WashText


# Shared with all deployments.
# Multiple content index for different types of content.
vmc_sheets = "1Cvmd1jI7-j-Ar_tEpE6vs8p8LklMwlX73Bg1dvEtU_M"

T_survey = "13aLV7tgTO6GNlI0zFG8gdq3BEl8PdX7kH5VEIXN5ssc"


# "filename" is how it will be generally named in the pipeline.
#
# "crowdin_name" will be the name of the file that is produced to send to the
# translators.
#
# "tags" are used to identify flows to be process. Possible values for tag 1:

#
# "split_no" is used to divide the file at the final step to get it to a manageable
# size that can be uploaded to RapidPro.
sources = [
    {
        "filename": "parenttext_all",
        "spreadsheet_ids": [
            T_survey,
            vmc_sheets
        ],
        # "archive": "parenttext_all.zip",
        #"archive": "https://drive.usercontent.google.com/download?id=1V9fQZ9ZrzwRkQWBtlHJ1it0Fe3hdtHs2&export=download&authuser=0&confirm=t&uuid=f9d65ff1-b210-4b61-a030-cd4a231c22ca&at=APZUnTVzz2FLSi1riCmRjCFI5vCx:1696348063599",  # noqa: E501
        "crowdin_name": "vmc_chatbot",
        "tags": [],
        "split_no": 1
    },
]

# Data used when modifying expiration times.
special_expiration = "./edits/specific_expiration.json"
default_expiration = 1440

# Model that is used as part of the process when the data is extracted from sheets.
model = "models.parenttext_models"

# Languages that will be looked for to localize back into the flows, "language" is the
# 3-letter code used in RapidPro, "code" is the 2 letter code used in CrowdIn.
languages = [
]

# Location where translations are stored, at the moment pointing to a locally cloned
# repo, should maybe be adapted so we can provide a link to an online repo.
translation_repo = "https://github.com/IDEMSInternational/plh-digital-content"
folder_within_repo = "translations/vmc"

# In one of the latter stages we have the option to modify the quick replies:
# 1 - We may want to remove the quick replies and add them to message text and give
#     numerical prompts to allow basic phone users to use the app - for this use
#     reference code "move"
# 2 - We may want to reformat the quick replies so that long ones are added to the
#     message text as above - for this use reference code "reformat"
# 3 - We may not want to do anything, for this use reference code "none"
qr_treatment = "reformat"

# This is the default phrase we want to add in if the quick replies are being moved to
# message text.
select_phrases = "./edits/select_phrases.json"

# If we are in scenario 1 above, we may wish to add some basic numerical quick
# replies back in, if so we need to specify add_selectors as True
add_selectors = "yes"

# Words we always want to keep as full quick replies are specified in this file.
special_words = "./edits/special_words.json"

# In scenario 2 we set limits on the number of quick replies and the length of the
# quick replies.
#   count_threshold (relates to number of quick replies)
#   length_threshold (relates to length of the longest quick reply)
# If the number of QRs is below or equal the count_threshold and the longest QR is
# shorter than or equal to the length_threshold then the QR are to be left in place
# the node will not be changed.
# In places where the QR are too long. We will make the changes to make the QRs
# numbers and add the number references to the message text as example 1.
count_threshold = "3"
length_threshold = "18"

# Google Sheet ID containing AB testing data.
# Same for all deployments.
ab_testing_sheet_ID = "1i_oqiJYkeoMsYdeFOcKlvvjnNCEdQnZlsm17fgNvK0s"
# Mexico specific.
localisation_sheet_ID = ""

# Google Sheet ID containing dict edits data.
# Same for all deployments.
eng_edits_sheet_ID = "1Ab8H_s26EuOiS4nZ6HGADjD4CZw55586LL66fl8tEWI"

transl_edits_sheet_ID = "195uFD9prl3qx5ziTIKeR9j_PDor01usfp4lrHMuu2s0"

# Data used in safeguarding script.
SG_flow_ID = "b83315a6-b25c-413a-9aa0-953bf60f223c"
SG_flow_name = "safeguarding_wfr_interaction"

# Path to file containing translated safeguarding words.
SG_path = "./edits/safeguarding_words.json"

# Names of redirect flows to be modified as part of safeguarding process.
redirect_flow_names = (
    '['
    '    "safeguarding_redirect_to_topic_all", '
    '    "safeguarding_redirect_to_topic_start", '
    '    "safeguarding_redirect_to_topic_trigger"'
    ']'
)

def create_config():
    return {
        "ab_testing_sheet_id": ab_testing_sheet_ID,
        "add_selectors": add_selectors,
        "count_threshold": count_threshold,
        "default_expiration": default_expiration,
        "eng_edits_sheet_id": eng_edits_sheet_ID,
        "folder_within_repo": folder_within_repo,
        "languages": languages,
        "length_threshold": length_threshold,
        "localisation_sheet_id": localisation_sheet_ID,
        "model": model,
        "qr_treatment": qr_treatment,
        "redirect_flow_names": redirect_flow_names,
        "select_phrases": select_phrases,
        "replace_phrases": "",
        "sg_flow_id": SG_flow_ID,
        "sg_flow_name": SG_flow_name,
        "sg_path": SG_path,
        "sources": sources,
        "special_expiration": special_expiration,
        "special_words": special_words,
        "translation_repo": translation_repo,
        "transl_edits_sheet_id": transl_edits_sheet_ID,
    }
