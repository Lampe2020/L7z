# Contribution guide   
> *Note that this guide will change as the project evolves, so check by from time to time!*   

Please be friendly to everyone you communicate with through this project. That means, no swearing in code or issue/PR 
comments, no snarky or snide comments, and of course mandatory use of common sense. This project should be a nice place 
to write code together with the goal of creating and maintaining a GUI for 7-zip for Linux and other *NIXes.   

## Code Guidelines   
* Tab width: 4 spaces (should when possible actually be inserted as spaces, not tab characters)   
* Max line length: 120 characters (the PyCharm default right margin line position)   
* Comments should be tab-aligned (the first character starting the comment should be on a position in the line 
  divisible by four if the first character in each line is character 0)   
* Use type annotations where possible

## About AI
Try to avoid having your code written by or edited by AI tooling. You may use AI to suggest things to you, but make 
sure to not blindly copy-paste code from the AI and try to submit it here. Even if the code works and it is not 
immediately obvious that it is AI-authored code, it still runs the risk of reducing the code quality and 
maintainability even lower than it already is.   
If code you submit is suspected to be largely or entirely written by AI, that is a valid reason to reject its merge.   

# Issues and PRs   
If you see a problem in the program and it hasn't been reported yet, feel free to open an Issue on GitHub.   
If you can fix any reported issues yourself, feel free to do so in your own fork of the project and then open a PR[^1] 
to get your fix merged into the main project. If you do so, please follow the above guidelines.   

# Translation
You are welcome to help with translation. Note that words enclosed in curly braces _MUST NOT_ be translated, as those 
are treated as variables and will stop L7z from functioning properly if they are translated!   
To get going with translating, run `gen-pot.sh` located in the project root and then use the generated `template.pot` 
located in the `locales` directory in the project root.   
When you encounter an ellipsis in a string, translate it as the ellipsis character (U+2026) if it is such in the 
original.



[^1]: PR stands for "Pull Request". You may know it as MR ("Merge Request") from other platforms, but in this project 
we call it PR inline with how GitHub calls it.  
