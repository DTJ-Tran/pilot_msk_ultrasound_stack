from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

def main():
    input_doc_path = Path("se_arch.pdf")

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    accelerator_options = AcceleratorOptions(device="cpu")

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )

    conversion_result = converter.convert(input_doc_path)
    doc = conversion_result.document

    md = doc.export_to_markdown()

    output_path = Path("se_arch.md")
    output_path.write_text(md, encoding="utf-8")

    # doc_conversion_secs = conversion_result.timings["pipeline_total"].times
    print(f"Saved markdown to {output_path}")
    # print(f"Conversion secs: {doc_conversion_secs}")

if __name__ == "__main__":
    main()