# How to Create a List of Figures in LaTeX

## Automatic Generation

The list of figures is **automatically generated** from all figures with captions in your document. You don't need to manually add entries!

## Current Setup

Your `thesis.tex` already includes:

```latex
\listoffigures
\newpage
```

This is placed after the table of contents and before your main content.

## How It Works

1. **Add figures with captions** in your document:
   ```latex
   \begin{figure}[h]
       \centering
       \includegraphics[width=0.8\textwidth]{figures/example.png}
       \caption{Your figure caption here.}
       \label{fig:example}
   \end{figure}
   ```

2. **Compile your document** (run `pdflatex` twice):
   ```bash
   pdflatex thesis.tex
   pdflatex thesis.tex
   ```

3. **The list appears automatically** in your PDF at the location where you placed `\listoffigures`.

## Requirements

For a figure to appear in the list of figures:
- ✅ Must be inside a `\begin{figure}...\end{figure}` environment
- ✅ Must have a `\caption{}` command
- ✅ The caption text will appear in the list

## Example Output

The list of figures will look like:

```
List of Figures

4.1  Example figure caption.  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
5.1  Experimental setup diagram  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
5.2  Results comparison  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
```

## Customization

### Change the Title

```latex
\renewcommand{\listfigurename}{List of Figures}  % Default
\renewcommand{\listfigurename}{Figures}          % Custom title
```

### Change Formatting

Add to your preamble:
```latex
\usepackage{tocloft}  % For more control

% Adjust spacing
\setlength{\cftfigindent}{0pt}      % Indentation
\setlength{\cftfignumwidth}{2.5em}  % Width for figure numbers
```

### Hide Specific Figures

If you don't want a figure in the list (but still want it in the document):
```latex
\caption*{This caption won't appear in list of figures}
```

Or use `\caption` without the figure environment:
```latex
\includegraphics{figures/image.png}
\captionof{figure}{This won't appear in list}  % Requires caption package
```

## Troubleshooting

### List is Empty
- Make sure your figures have `\caption{}` commands
- Make sure figures are inside `\begin{figure}...\end{figure}` environments
- Run `pdflatex` **twice** to update the list

### List Not Updating
- Delete `.lof` file and recompile
- Run `pdflatex` twice (first pass creates `.lof`, second pass includes it)

### Figures Not Numbered Correctly
- Figures are numbered by chapter (e.g., 4.1, 4.2 in Chapter 4)
- To number continuously throughout document, add to preamble:
  ```latex
  \usepackage{chngcntr}
  \counterwithout{figure}{chapter}
  ```

## Complete Example

```latex
\documentclass{report}

\begin{document}

\tableofcontents
\newpage
\listoffigures    % List of figures here
\newpage

\chapter{Introduction}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.5\textwidth]{figures/diagram.pdf}
    \caption{System architecture diagram.}
    \label{fig:architecture}
\end{figure}

\chapter{Results}

\begin{figure}[h]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/results.png}
    \caption{Experimental results showing performance metrics.}
    \label{fig:results}
\end{figure}

\end{document}
```

After compiling twice, the list of figures will automatically show:
- Figure 1.1: System architecture diagram (page X)
- Figure 2.1: Experimental results showing performance metrics (page Y)

## Your Current Status

✅ `\listoffigures` is already in your thesis.tex  
✅ It's placed correctly after table of contents  
✅ Your example figure will appear in the list  
✅ Just compile with `pdflatex thesis.tex` (twice) to see it!

