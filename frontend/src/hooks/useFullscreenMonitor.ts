import { useEffect, useRef, useState } from 'react';
import { apiClient, endpoints } from '@/api/endpoints';

interface FullscreenMonitorOptions {
  candidateEmail: string;
  maxExits?: number;
  onRejected?: () => void;
}

export const useFullscreenMonitor = ({ 
  candidateEmail, 
  maxExits = 3,
  onRejected 
}: FullscreenMonitorOptions) => {
  const [exitCount, setExitCount] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isRejected, setIsRejected] = useState(false);
  const hasRequestedFullscreen = useRef(false);

  // Request fullscreen on mount
  useEffect(() => {
    if (!hasRequestedFullscreen.current) {
      hasRequestedFullscreen.current = true;
      requestFullscreen();
    }
  }, []);

  // Monitor fullscreen changes
  useEffect(() => {
    const handleFullscreenChange = async () => {
      const isCurrentlyFullscreen = !!(
        document.fullscreenElement ||
        (document as any).webkitFullscreenElement ||
        (document as any).mozFullScreenElement ||
        (document as any).msFullscreenElement
      );

      setIsFullscreen(isCurrentlyFullscreen);

      // If exiting fullscreen (and not first time)
      if (!isCurrentlyFullscreen && hasRequestedFullscreen.current) {
        const newCount = exitCount + 1;
        setExitCount(newCount);

        console.warn(`Fullscreen exit detected. Count: ${newCount}/${maxExits}`);

        // Check if exceeded limit
        if (newCount >= maxExits) {
          console.error('Maximum fullscreen exits exceeded. Marking candidate as rejected.');
          await markCandidateAsRejected();
          setIsRejected(true);
          onRejected?.();
        } else {
          // Request fullscreen again
          setTimeout(() => {
            requestFullscreen();
          }, 500);
        }
      }
    };

    // Add event listeners for fullscreen changes
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', handleFullscreenChange);
    document.addEventListener('MSFullscreenChange', handleFullscreenChange);

    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
      document.removeEventListener('mozfullscreenchange', handleFullscreenChange);
      document.removeEventListener('MSFullscreenChange', handleFullscreenChange);
    };
  }, [exitCount, maxExits, onRejected]);

  const requestFullscreen = () => {
    const elem = document.documentElement;

    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch((err) => {
        console.error('Error attempting to enable fullscreen:', err);
      });
    } else if ((elem as any).webkitRequestFullscreen) {
      (elem as any).webkitRequestFullscreen();
    } else if ((elem as any).mozRequestFullScreen) {
      (elem as any).mozRequestFullScreen();
    } else if ((elem as any).msRequestFullscreen) {
      (elem as any).msRequestFullscreen();
    }
  };

  const markCandidateAsRejected = async () => {
    if (!candidateEmail) {
      console.error('Cannot mark candidate as rejected: email not provided');
      return;
    }

    try {
      await apiClient.post(endpoints.rejectCandidate, {
        email: candidateEmail,
        reason: 'malpractice_fullscreen_exit',
      });
      console.log('Candidate marked as rejected in database');
    } catch (error) {
      console.error('Error marking candidate as rejected:', error);
    }
  };

  return {
    exitCount,
    maxExits,
    isFullscreen,
    isRejected,
    requestFullscreen,
  };
};
