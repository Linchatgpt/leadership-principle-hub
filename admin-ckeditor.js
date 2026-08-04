import { ClassicEditor, Essentials, Paragraph, Bold, Italic, Font, Heading, BlockQuote, Link, List } from 'ckeditor5';
Object.assign(window, { ClassicEditor, Essentials, Paragraph, Bold, Italic, Font, Heading, BlockQuote, Link, List });
window.createLocalEditor = (element, data) => ClassicEditor.create(element, {
  initialData: data, licenseKey: 'GPL', plugins: [Essentials, Paragraph, Bold, Italic, Font, Heading, BlockQuote, Link, List],
  toolbar: ['undo','redo','|','heading','fontFamily','fontSize','fontColor','bold','italic','link','bulletedList','numberedList','blockQuote'],
  fontSize: { options: [9, 11, 13, 16, 20, 24, 32], supportAllValues: true }, fontFamily: { options: ['default','Arial','Georgia','Noto Sans TC','Courier New'] }
});
