#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module progress - Hiển thị tiến trình xử lý

Mục đích: Cải thiện UX bằng cách cho người dùng biết tiến độ
Lý do: Các thao tác xử lý nhiều file có thể mất thời gian
"""

import sys
import time
from typing import Optional
from .colors import Colors


class ProgressBar:
    """
    Class hiển thị progress bar trong terminal
    
    Mục đích: Giúp người dùng theo dõi tiến độ xử lý
    """
    
    def __init__(self, total: int, prefix: str = '', suffix: str = '', 
                 length: int = 50, fill: str = '█', show_percentage: bool = True):
        """
        Khởi tạo progress bar
        
        Args:
            total: Tổng số items cần xử lý
            prefix: Text hiển thị trước progress bar
            suffix: Text hiển thị sau progress bar
            length: Độ dài của progress bar (số ký tự)
            fill: Ký tự dùng để fill progress bar
            show_percentage: Có hiển thị phần trăm không
        
        Giải thích:
        - total: Số items cần xử lý (vd: số file cần copy)
        - prefix/suffix: Thông tin bổ sung (vd: "Đang xử lý: " / " hoàn thành")
        - length: Độ dài visual của bar
        - fill: Ký tự hiển thị phần đã hoàn thành
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.show_percentage = show_percentage
        self.current = 0
        self.start_time = time.time()
    
    def update(self, current: Optional[int] = None, message: str = '') -> None:
        """
        Cập nhật progress bar
        
        Args:
            current: Số item hiện tại (nếu None thì tự động tăng 1)
            message: Thông báo bổ sung hiển thị sau progress bar
        
        Giải thích:
        - Nếu current được truyền vào, dùng giá trị đó
        - Nếu không, tự động tăng counter lên 1
        - Tính phần trăm hoàn thành
        - Hiển thị progress bar với format đẹp
        """
        if current is not None:
            self.current = current
        else:
            self.current += 1
        
        # Đảm bảo không vượt quá total
        if self.current > self.total:
            self.current = self.total
        
        # Tính phần trăm
        percent = 100 * (self.current / float(self.total))
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # Tính thời gian còn lại
        elapsed_time = time.time() - self.start_time
        if self.current > 0:
            avg_time_per_item = elapsed_time / self.current
            remaining_items = self.total - self.current
            eta_seconds = avg_time_per_item * remaining_items
            eta_str = self._format_time(eta_seconds)
        else:
            eta_str = "N/A"
        
        # Xây dựng output string với màu sắc
        output_parts = []
        
        if self.prefix:
            output_parts.append(Colors.info(self.prefix))
        
        # Colorize progress bar với design đẹp hơn
        filled_part = Colors.success(self.fill * filled_length)
        empty_part = Colors.muted('─' * (self.length - filled_length))
        # Thêm gradient effect
        if filled_length > 0:
            # Last character có thể là một nửa nếu cần
            colored_bar = f'{Colors.primary("╞")}{filled_part}{empty_part}{Colors.primary("╡")}'
        else:
            colored_bar = f'{Colors.primary("╞")}{empty_part}{Colors.primary("╡")}'
        output_parts.append(colored_bar)
        
        if self.show_percentage:
            percent_str = f'{percent:.1f}%'
            if percent >= 100:
                output_parts.append(Colors.success(percent_str))
            elif percent >= 50:
                output_parts.append(Colors.info(percent_str))
            else:
                output_parts.append(Colors.warning(percent_str))
        
        count_str = f'({self.current}/{self.total})'
        output_parts.append(Colors.muted(count_str))
        
        if self.current < self.total:
            eta_str_colored = Colors.muted(f'ETA: {eta_str}')
            output_parts.append(eta_str_colored)
        
        if message:
            output_parts.append(Colors.primary(f'- {message}'))
        
        if self.suffix:
            output_parts.append(Colors.muted(self.suffix))
        
        # In ra và xóa dòng cũ
        output = ' '.join(output_parts)
        print(f'\r{output}', end='', flush=True)
        
        # Xuống dòng khi hoàn thành
        if self.current >= self.total:
            print()
    
    def _format_time(self, seconds: float) -> str:
        """
        Format thời gian thành dạng dễ đọc
        
        Args:
            seconds: Số giây
        
        Returns:
            str: Thời gian đã format (vd: "2m 30s")
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def finish(self, message: str = "Hoàn thành!") -> None:
        """
        Kết thúc progress bar và hiển thị thông báo
        
        Args:
            message: Thông báo khi hoàn thành
        """
        self.update(self.total, message)
        
        # Hiển thị tổng thời gian với box đẹp
        total_time = time.time() - self.start_time
        time_str = self._format_time(total_time)
        print()
        print(Colors.success(f"  ✅ {Colors.bold(message)}"))
        print(Colors.muted(f"  ⏱️  Tổng thời gian: {Colors.info(time_str)}"))


class Spinner:
    """
    Class hiển thị spinner animation cho các thao tác không biết thời gian
    
    Mục đích: Cho người dùng biết chương trình vẫn đang chạy
    Lý do: Một số thao tác không biết trước thời gian hoàn thành
    """
    
    def __init__(self, message: str = "Đang xử lý..."):
        """
        Khởi tạo spinner
        
        Args:
            message: Thông báo hiển thị cùng spinner
        """
        self.message = message
        self.is_spinning = False
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_frame = 0
    
    def start(self) -> None:
        """Bắt đầu hiển thị spinner"""
        self.is_spinning = True
        self._spin()
    
    def stop(self, final_message: str = "Hoàn thành!") -> None:
        """
        Dừng spinner và hiển thị thông báo cuối
        
        Args:
            final_message: Thông báo khi hoàn thành
        """
        self.is_spinning = False
        print(f'\r{final_message}' + ' ' * 20)
    
    def _spin(self) -> None:
        """Hiển thị frame tiếp theo của spinner"""
        if self.is_spinning:
            frame = self.frames[self.current_frame]
            colored_frame = Colors.info(frame)
            colored_message = Colors.primary(self.message)
            print(f'\r{colored_frame} {colored_message}', end='', flush=True)
            self.current_frame = (self.current_frame + 1) % len(self.frames)


def simple_progress(iterable, prefix: str = '', total: Optional[int] = None):
    """
    Generator đơn giản hiển thị progress cho vòng lặp
    
    Args:
        iterable: Iterable cần loop
        prefix: Prefix hiển thị
        total: Tổng số items (nếu không biết trước)
    
    Yields:
        item: Từng item trong iterable
    
    Ví dụ:
        for file in simple_progress(file_list, prefix="Xử lý file"):
            process_file(file)
    
    Giải thích:
    - Wrapper cho iterable, tự động cập nhật progress
    - Dễ sử dụng hơn ProgressBar cho các trường hợp đơn giản
    """
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            # Nếu không có len(), dùng counter
            total = 0
            for _ in iterable:
                total += 1
    
    bar = ProgressBar(total, prefix=prefix)
    
    for item in iterable:
        yield item
        bar.update()
    
    bar.finish()

