# How to Insert Images in LaTeX

## Basic Syntax

The `graphicx` package is already included in your thesis.tex file. Use the `\includegraphics` command to insert images.

## Supported Formats

LaTeX supports:
- **PDF** (recommended for vector graphics)
- **PNG** (for photos and screenshots)
- **JPG/JPEG** (for photos)
- **EPS** (older format, less common now)

## Basic Image Insertion

### Simple Image (no caption)

```latex
\includegraphics{figures/myimage.png}
```

### Image with Figure Environment (recommended)

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/myimage.png}
    \caption{Your figure caption here.}
    \label{fig:myimage}
\end{figure}
```

## Image Sizing Options

### By Width (relative to text width)
```latex
\includegraphics[width=0.5\textwidth]{figures/image.png}  % 50% of text width
\includegraphics[width=0.8\textwidth]{figures/image.png}  % 80% of text width
```

### By Height
```latex
\includegraphics[height=5cm]{figures/image.png}
\includegraphics[height=0.5\textheight]{figures/image.png}
```

### By Scale
```latex
\includegraphics[scale=0.5]{figures/image.png}  % 50% of original size
\includegraphics[scale=1.2]{figures/image.png}  % 120% of original size
```

### Specific Dimensions
```latex
\includegraphics[width=10cm,height=8cm]{figures/image.png}
```

## Figure Placement Options

The `[h]` in `\begin{figure}[h]` controls placement:

- `h` - here (at the current position)
- `t` - top of page
- `b` - bottom of page
- `p` - on a separate page of floats
- `!` - override LaTeX's placement rules
- `H` - HERE (requires `\usepackage{float}`) - forces exact position

Examples:
```latex
\begin{figure}[htbp]  % Try here, then top, then bottom, then float page
\begin{figure}[H]     % Exact position (requires float package)
```

## Multiple Images Side by Side

### Using subfigure (requires subcaption package)
```latex
\usepackage{subcaption}

\begin{figure}[h]
    \centering
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{figures/image1.png}
        \caption{First image}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.45\textwidth}
        \includegraphics[width=\textwidth]{figures/image2.png}
        \caption{Second image}
    \end{subfigure}
    \caption{Two images side by side}
    \label{fig:twoimages}
\end{figure}
```

## Referencing Figures

After labeling a figure with `\label{fig:myimage}`, reference it:

```latex
As shown in Figure~\ref{fig:myimage}, we can see...
```

## Best Practices

1. **Use PDF for vector graphics** (diagrams, plots) - scales perfectly
2. **Use PNG/JPG for photos** - better compression
3. **Keep images in a `figures/` folder** - organized structure
4. **Use relative paths** - `figures/image.png` not `/full/path/to/image.png`
5. **Always include captions** - helps readers understand the figure
6. **Use descriptive labels** - `\label{fig:results_comparison}` not `\label{fig:1}`

## Example: Complete Figure

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/experimental_setup.pdf}
    \caption{Schematic diagram of the experimental setup showing the 
             radar transmitter, receiver, and target configuration.}
    \label{fig:experimental_setup}
\end{figure}

The experimental setup is illustrated in Figure~\ref{fig:experimental_setup}.
```

## Troubleshooting

- **Image not found**: Check the path is correct relative to your .tex file
- **Image too large**: Use `width=0.8\textwidth` or `scale=0.5`
- **Image appears in wrong place**: Use `[H]` placement or `\FloatBarrier` from placeins package
- **Low quality**: Use PDF format for vector graphics, or ensure PNG/JPG has sufficient resolution (300 DPI for print)

