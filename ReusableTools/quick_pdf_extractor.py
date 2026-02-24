"""
Quick PDF Extractor - Fast, targeted content extraction

Purpose: Quick keyword-based searches for specific information
Use when: You need specific answers about particular topics
"""

import PyPDF2
import re
import os
from typing import List, Dict, Optional

class QuickPDFExtractor:
    """Fast, targeted PDF content extraction"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.total_pages = self._get_page_count()
    
    def _get_page_count(self) -> int:
        """Get total page count quickly"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception:
            return 0
    
    def extract_targeted_content(self, keywords: List[str], max_results: int = 3) -> Dict:
        """Extract content around specific keywords"""
        if not keywords or self.total_pages == 0:
            return {'error': 'No keywords provided or PDF not accessible'}
        
        # Smart page range - skip intro, focus on content
        start_page = min(3, self.total_pages // 10)
        end_page = min(start_page + 30, self.total_pages)  # Limit scope for speed
        
        results = []
        patterns = [re.compile(rf'\b{re.escape(kw)}\b', re.IGNORECASE) for kw in keywords]
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(start_page, end_page):
                    if len(results) >= max_results:
                        break
                    
                    try:
                        page_text = pdf_reader.pages[page_num].extract_text()
                        
                        # Quick pre-filter
                        if not any(kw.lower() in page_text.lower() for kw in keywords):
                            continue
                        
                        # Find relevant sections
                        sections = self._extract_relevant_sections(page_text, patterns, keywords)
                        
                        if sections:
                            results.append({
                                'page': page_num + 1,
                                'sections': sections[:2],  # Top 2 per page
                                'keywords_found': list(set([s['keyword'] for s in sections]))
                            })
                    
                    except Exception:
                        continue
        
        except Exception as e:
            return {'error': f'Failed to read PDF: {e}'}
        
        return {
            'filename': os.path.basename(self.pdf_path),
            'keywords_searched': keywords,
            'pages_searched': f"{start_page+1}-{end_page}",
            'results_found': len(results),
            'results': results
        }
    
    def extract_toc_guided_content(self, keywords: List[str], max_results: int = 3) -> Dict:
        """Extract content using TOC guidance for better targeting"""
        if not keywords or self.total_pages == 0:
            return {'error': 'No keywords provided or PDF not accessible'}
        
        # First, get TOC information
        toc_info = self._get_toc_info()
        
        # Find relevant sections based on TOC
        relevant_sections = self._find_relevant_toc_sections(keywords, toc_info)
        
        # If we found relevant sections, focus search there
        if relevant_sections:
            return self._search_targeted_sections(keywords, relevant_sections, max_results)
        else:
            # Fall back to general search
            return self.extract_targeted_content(keywords, max_results)
    
    def _get_toc_info(self) -> Dict:
        """Extract TOC information for guidance"""
        toc_info = {'sections': [], 'has_toc': False}
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Look for TOC in first 10 pages
                for page_num in range(min(10, self.total_pages)):
                    page_text = pdf_reader.pages[page_num].extract_text()
                    
                    if 'contents' in page_text.lower() or 'table of contents' in page_text.lower():
                        toc_info['has_toc'] = True
                        toc_info['sections'] = self._extract_toc_sections(page_text)
                        break
        
        except Exception:
            pass
        
        return toc_info
    
    def _extract_toc_sections(self, text: str) -> List[Dict]:
        """Extract TOC sections with page hints and improved detection"""
        sections = []
        lines = text.split('\n')
        
        for line in lines:
            line_clean = line.strip()
            
            # Skip very short lines
            if len(line_clean) < 5:
                continue
            
            # Enhanced TOC entry detection
            page_num = None
            title = line_clean
            
            # Pattern 1: Lines with dots leading to page numbers (...123)
            dots_match = re.search(r'\.{3,}\s*(\d+)$', line_clean)
            if dots_match:
                page_num = int(dots_match.group(1))
                title = re.sub(r'\.{3,}\s*\d+$', '', line_clean).strip()
            
            # Pattern 2: Lines ending with page numbers (   123)
            elif re.search(r'\s+(\d+)$', line_clean):
                page_match = re.search(r'\s+(\d+)$', line_clean)
                page_num = int(page_match.group(1))
                title = re.sub(r'\s+\d+$', '', line_clean).strip()
            
            # Pattern 3: Tab-separated content with page numbers
            elif '\t' in line_clean:
                parts = line_clean.split('\t')
                if len(parts) >= 2 and parts[-1].strip().isdigit():
                    page_num = int(parts[-1].strip())
                    title = '\t'.join(parts[:-1]).strip()
            
            # Pattern 4: Lines with chapter/section keywords (even without page numbers)
            elif any(keyword in line_clean.lower() for keyword in [
                'chapter', 'section', 'appendix', 'part', 'overview',
                'introduction', 'getting started', 'configuration', 'setup'
            ]):
                # Try to extract page number if present
                page_match = re.search(r'(\d+)', line_clean)
                if page_match:
                    potential_page = int(page_match.group(1))
                    if potential_page > 0 and potential_page < 9999:  # Reasonable page range
                        page_num = potential_page
            
            # Only include if we have a meaningful title
            if len(title) > 5 and len(title) < 200:
                # Additional filtering for likely TOC entries
                is_likely_toc = False
                
                # Check for TOC indicators
                if page_num is not None:
                    is_likely_toc = True
                elif any(keyword in title.lower() for keyword in [
                    'chapter', 'section', 'appendix', 'overview', 'introduction',
                    'getting started', 'configuration', 'setup', 'installation',
                    'troubleshooting', 'reference', 'guide', 'manual'
                ]):
                    is_likely_toc = True
                elif re.match(r'^\d+\.?\d*\s+[A-Z]', title):  # Numbered sections
                    is_likely_toc = True
                elif title.count('.') <= 2 and not title.endswith('.'):  # Not prose
                    is_likely_toc = True
                
                if is_likely_toc:
                    sections.append({
                        'title': title,
                        'page': page_num,
                        'keywords': self._extract_section_keywords(title)
                    })
        
        return sections[:20]  # Limit sections for performance
    
    def _extract_section_keywords(self, title: str) -> List[str]:
        """Extract keywords from section title"""
        # Remove common words and numbers
        words = re.findall(r'\b[A-Za-z]{3,}\b', title.lower())
        common_words = {'the', 'and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'chapter', 'section'}
        return [word for word in words if word not in common_words][:3]
    
    def _find_relevant_toc_sections(self, keywords: List[str], toc_info: Dict) -> List[Dict]:
        """Find TOC sections relevant to search keywords"""
        if not toc_info['has_toc'] or not toc_info['sections']:
            return []
        
        relevant_sections = []
        keywords_lower = [kw.lower() for kw in keywords]
        
        for section in toc_info['sections']:
            # Check if any keyword matches section title or keywords
            title_lower = section['title'].lower()
            section_keywords = section.get('keywords', [])
            
            relevance_score = 0
            for kw in keywords_lower:
                if kw in title_lower:
                    relevance_score += 3
                elif any(kw in sk for sk in section_keywords):
                    relevance_score += 1
            
            if relevance_score > 0:
                section['relevance_score'] = relevance_score
                relevant_sections.append(section)
        
        # Sort by relevance and return top sections
        relevant_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_sections[:5]
    
    def _search_targeted_sections(self, keywords: List[str], sections: List[Dict], max_results: int) -> Dict:
        """Search in specific sections identified by TOC with improved page targeting"""
        results = []
        patterns = [re.compile(rf'\b{re.escape(kw)}\b', re.IGNORECASE) for kw in keywords]
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for section in sections:
                    if len(results) >= max_results:
                        break
                    
                    # Improved page targeting based on TOC
                    if section.get('page'):
                        # Use exact page from TOC
                        target_page = section['page'] - 1  # Convert to 0-based
                        start_page = max(0, target_page - 1)  # 1 page before
                        end_page = min(self.total_pages, target_page + 5)  # 5 pages after
                    else:
                        # Estimate based on section position in TOC
                        section_index = sections.index(section)
                        estimated_page = max(5, (section_index + 1) * (self.total_pages // len(sections)))
                        start_page = max(0, estimated_page - 3)
                        end_page = min(self.total_pages, estimated_page + 8)
                    
                    section_found = False
                    for page_num in range(start_page, end_page):
                        try:
                            page_text = pdf_reader.pages[page_num].extract_text()
                            
                            # Enhanced pre-filtering
                            page_lower = page_text.lower()
                            keyword_matches = sum(1 for kw in keywords if kw.lower() in page_lower)
                            
                            if keyword_matches == 0:
                                continue
                            
                            # Look for section title in page (confirms we're in right section)
                            section_title_words = section['title'].lower().split()[:3]  # First 3 words
                            title_match_score = sum(1 for word in section_title_words 
                                                  if len(word) > 2 and word in page_lower)
                            
                            # Find keyword matches
                            sections_found = self._extract_relevant_sections(page_text, patterns, keywords)
                            
                            if sections_found:
                                result_entry = {
                                    'page': page_num + 1,
                                    'section_context': section['title'],
                                    'sections': sections_found[:2],
                                    'keywords_found': list(set([s['keyword'] for s in sections_found])),
                                    'title_match_score': title_match_score,
                                    'keyword_density': keyword_matches / max(1, len(page_text.split()))
                                }
                                
                                results.append(result_entry)
                                section_found = True
                                break  # Found content in this section, move to next
                        
                        except Exception:
                            continue
                    
                    # If no content found in expected pages, do a broader search for this section
                    if not section_found and len(results) < max_results:
                        broader_results = self._broader_section_search(
                            keywords, section, patterns, pdf_reader
                        )
                        if broader_results:
                            results.extend(broader_results[:1])  # Add top result
        
        except Exception as e:
            return {'error': f'Failed to search targeted sections: {e}'}
        
        # Sort results by relevance (title match score + keyword density)
        results.sort(key=lambda x: (x.get('title_match_score', 0) + x.get('keyword_density', 0)), reverse=True)
        
        return {
            'filename': os.path.basename(self.pdf_path),
            'keywords_searched': keywords,
            'toc_guided': True,
            'sections_targeted': [s['title'] for s in sections],
            'results_found': len(results),
            'results': results[:max_results]
        }
    
    def _broader_section_search(self, keywords: List[str], section: Dict, patterns: List, pdf_reader) -> List[Dict]:
        """Perform broader search when targeted search fails"""
        results = []
        
        # Search more pages around estimated location
        section_keywords = section.get('keywords', [])
        
        # Search in chunks across the document
        chunk_size = 20
        for chunk_start in range(0, self.total_pages, chunk_size):
            chunk_end = min(chunk_start + chunk_size, self.total_pages)
            
            for page_num in range(chunk_start, chunk_end):
                try:
                    page_text = pdf_reader.pages[page_num].extract_text()
                    page_lower = page_text.lower()
                    
                    # Check for section keywords AND search keywords
                    section_relevance = sum(1 for kw in section_keywords if kw in page_lower)
                    keyword_matches = sum(1 for kw in keywords if kw.lower() in page_lower)
                    
                    if section_relevance > 0 and keyword_matches > 0:
                        sections_found = self._extract_relevant_sections(page_text, patterns, keywords)
                        
                        if sections_found:
                            results.append({
                                'page': page_num + 1,
                                'section_context': f"{section['title']} (broader search)",
                                'sections': sections_found[:1],
                                'keywords_found': list(set([s['keyword'] for s in sections_found])),
                                'broader_search': True
                            })
                            break  # Found something, move to next chunk
                
                except Exception:
                    continue
            
            if results:  # Found something, stop searching
                break
        
        return results

    def _extract_relevant_sections(self, text: str, patterns: List, keywords: List[str]) -> List[Dict]:
        """Extract sections around keyword matches"""
        sections = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if len(line.strip()) < 10:  # Skip short lines
                continue
            
            for pattern, keyword in zip(patterns, keywords):
                if pattern.search(line):
                    # Get context around match
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = ' '.join(lines[context_start:context_end]).strip()
                    
                    # Clean and limit context
                    context = re.sub(r'\s+', ' ', context)  # Normalize whitespace
                    if len(context) > 300:
                        context = context[:300] + "..."
                    
                    sections.append({
                        'keyword': keyword,
                        'context': context,
                        'line_number': i + 1
                    })
                    
                    if len(sections) >= 5:  # Limit per page
                        return sections
        
        return sections

def quick_extract_with_toc(pdf_path: str, keywords: List[str], max_results: int = 3) -> Dict:
    """Quick extraction with TOC guidance"""
    extractor = QuickPDFExtractor(pdf_path)
    return extractor.extract_toc_guided_content(keywords, max_results)

def quick_extract(pdf_path: str, keywords: List[str], max_results: int = 3) -> Dict:
    """Legacy function - quick keyword extraction (maintained for compatibility)"""
    extractor = QuickPDFExtractor(pdf_path)
    return extractor.extract_targeted_content(keywords, max_results)

# Test function
def test_quick_extractor():
    """Test the quick extractor"""
    pdf_path = r"D:\Kiro\ANA-050_to_Solution_ReferenceDocuments\Web_UI_UserGuide.pdf"
    
    print("=== Quick PDF Extractor Test ===")
    
    # Test targeted extraction
    result = quick_extract(pdf_path, ["navigation", "menu", "interface"], max_results=2)
    
    if 'error' not in result:
        print(f"File: {result['filename']}")
        print(f"Pages searched: {result['pages_searched']}")
        print(f"Results found: {result['results_found']}")
        
        for i, res in enumerate(result['results'], 1):
            print(f"\n[Result {i}] Page {res['page']}")
            print(f"Keywords: {', '.join(res['keywords_found'])}")
            for section in res['sections']:
                print(f"  - {section['keyword']}: {section['context'][:150]}...")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_quick_extractor()